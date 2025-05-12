from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.tasks import models
from apps.tasks import serializers


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["category", "education_level", "type"]
