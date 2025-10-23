from django.contrib import admin
from .models import Category, CategorySimilarity

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "position", "depth", "path")
    list_filter = ("parent", "depth")
    search_fields = ("name",)

@admin.register(CategorySimilarity)
class CategorySimilarityAdmin(admin.ModelAdmin):
    list_display = ("id", "cat_left", "cat_right")
    search_fields = ("cat_left__name", "cat_right__name")