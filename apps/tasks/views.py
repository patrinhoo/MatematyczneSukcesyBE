from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.tasks.models.task_orm import TaskOrm
from apps.tasks.serializers.task import TaskSerializer


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TaskOrm.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["category", "education_level", "type"]
