from rest_framework import viewsets

from apps.core.models.category_orm import CategoryOrm
from apps.core.serializers.category import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryOrm.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
