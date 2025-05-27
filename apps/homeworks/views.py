from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from apps.homeworks import models
from apps.homeworks import serializers


class HomeworkViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.HomeworkSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["status"]

    def get_queryset(self):
        return (
            models.Homework.objects.filter(assigned_to=self.request.user)
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
        return models.HomeworkTask.objects.filter(
            homework__assigned_to=self.request.user
        ).select_related("homework", "task")

    def get_serializer_class(self):
        if self.action == "partial_update":
            return serializers.HomeworkTaskSolutionUploadSerializer
        return serializers.HomeworkTaskSerializer
