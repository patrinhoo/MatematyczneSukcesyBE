from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from apps.homeworks.filters.homework import HomeworkFilter
from apps.homeworks.models.homework_orm import HomeworkOrm
from apps.homeworks.models.homework_task_orm import HomeworkTaskOrm
from apps.homeworks.serializers.homework import HomeworkSerializer
from apps.homeworks.serializers.homework_task import (
    HomeworkTaskSerializer,
    HomeworkTaskSolutionUploadSerializer,
)


class HomeworkViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = HomeworkSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_class = HomeworkFilter

    def get_queryset(self):
        return (
            HomeworkOrm.objects.filter(assigned_to=self.request.user)
            .select_related("assigned_by", "assigned_to")
            .prefetch_related("homework_tasks__task")
        )


class HomeworkTaskViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    http_method_names = ["get", "patch"]

    def get_queryset(self):
        return HomeworkTaskOrm.objects.filter(
            homework__assigned_to=self.request.user
        ).select_related("homework", "task")

    def get_serializer_class(self):
        if self.action == "partial_update":
            return HomeworkTaskSolutionUploadSerializer
        return HomeworkTaskSerializer
