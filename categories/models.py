from django.db import models, transaction


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)

    parent = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)

    depth = models.PositiveIntegerField(default=0, editable=False)
    path = models.CharField(max_length=1024, editable=False, db_index=True)

    class Meta:
        ordering = ["parent_id", "position", "name"]
        indexes = [
            models.Index(fields=["parent"]),
            models.Index(fields=["depth"]),
            models.Index(fields=["path"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    def _compute_depth_and_path(self, parent):
        if parent:
            return parent.depth + 1, f"{parent.path}{self.pk}/"
        return 0, f"/{self.pk}/"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        parent_before = None if is_new else Category.objects.filter(pk=self.pk).values_list("parent_id",
                                                                                            flat=True).first()
        super().save(*args, **kwargs)  # need PK

        # guard: cannot parent under own subtree
        if self.parent and str(self.pk) in (self.parent.path or ""):
            raise ValueError("Cannot move a node under its own subtree.")

        # update self path/depth
        depth, path = self._compute_depth_and_path(self.parent)
        if self.depth != depth or self.path != path:
            Category.objects.filter(pk=self.pk).update(depth=depth, path=path)
            self.depth, self.path = depth, path

        # if parent changed or new, update descendants in bulk
        if is_new or parent_before != self.parent_id:
            old_prefix = None  # on create we don’t have old path
            new_prefix = self.path
            with transaction.atomic():
                descendants = Category.objects.filter(path__startswith=new_prefix).exclude(pk=self.pk)
                # recompute depth/path for descendants
                for child in self.children.all().order_by("depth"):
                    child._cascade_repath()

    def _cascade_repath(self):
        depth, path = self._compute_depth_and_path(self.parent)
        if self.depth != depth or self.path != path:
            Category.objects.filter(pk=self.pk).update(depth=depth, path=path)
            self.depth, self.path = depth, path
        for c in self.children.all():
            c._cascade_repath()


class CategorySimilarity(models.Model):
    cat_left = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="similar_left")
    cat_right = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="similar_right")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cat_left", "cat_right"], name="unique_similarity_pair")
        ]
        indexes = [
            models.Index(fields=["cat_left"]),
            models.Index(fields=["cat_right"]),
        ]

    def clean(self):
        if self.cat_left_id == self.cat_right_id:
            raise ValueError("Category cannot be similar to itself.")
        # normalize ordering to enforce bidirectionality
        if self.cat_left_id and self.cat_right_id and self.cat_left_id > self.cat_right_id:
            self.cat_left_id, self.cat_right_id = self.cat_right_id, self.cat_left_id

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
