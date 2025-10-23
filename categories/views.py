from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, CategorySimilarity
from .serializers import CategorySerializer, CategorySimilaritySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().select_related("parent")
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        parent_id = self.request.query_params.get("parent")
        depth = self.request.query_params.get("depth")
        subtree_of = self.request.query_params.get("subtree_of")
        ancestors_of = self.request.query_params.get("ancestors_of")
        search = self.request.query_params.get("search")

        if parent_id:
            qs = qs.filter(parent_id=parent_id)
        if depth is not None:
            qs = qs.filter(depth=int(depth))
        if subtree_of:
            try:
                root = Category.objects.get(pk=int(subtree_of))
                qs = qs.filter(path__startswith=root.path)
            except Category.DoesNotExist:
                qs = qs.none()
        if ancestors_of:
            try:
                node = Category.objects.get(pk=int(ancestors_of))
                # ancestors are all ids inside path except the node itself
                ids = [int(x) for x in node.path.strip("/").split("/")[:-1]] if node.path else []
                qs = qs.filter(pk__in=ids)
            except Category.DoesNotExist:
                qs = qs.none()
        if search:
            qs = qs.filter(name__icontains=search)

        return qs

    @action(detail=True, methods=["post"])
    def move(self, request, pk=None):
        node = self.get_object()
        new_parent_id = request.data.get("new_parent_id")
        new_position = request.data.get("new_position", node.position)
        try:
            node.parent_id = int(new_parent_id) if new_parent_id is not None else None
            node.position = int(new_position)
            node.save()
            return Response(self.get_serializer(node).data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def similar(self, request, pk=None):
        node_id = int(pk)
        neighbors = CategorySimilarity.objects.filter(
            Q(cat_left_id=node_id) | Q(cat_right_id=node_id)
        )
        ids = set()
        for e in neighbors:
            ids.add(e.cat_left_id if e.cat_left_id != node_id else e.cat_right_id)
            ids.add(e.cat_right_id if e.cat_right_id != node_id else e.cat_left_id)
        cats = Category.objects.filter(pk__in=ids)
        return Response(CategorySerializer(cats, many=True).data)


class CategorySimilarityViewSet(viewsets.ModelViewSet):
    queryset = CategorySimilarity.objects.all().select_related("cat_left", "cat_right")
    serializer_class = CategorySimilaritySerializer
