from rest_framework import serializers

from apps.core.models.category_orm import CategoryOrm


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryOrm
        fields = "__all__"
