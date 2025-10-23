from rest_framework import serializers
from .models import Category, CategorySimilarity


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "image", "parent", "position", "depth", "path"]
        read_only_fields = ["depth", "path"]


class CategorySimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySimilarity
        fields = ["id", "cat_left", "cat_right"]
