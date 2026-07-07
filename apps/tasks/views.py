import json

from rest_framework import mixins, viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from apps.tasks.domain.enums.tasks import TaskStatus
from apps.tasks.models.task_orm import TaskOrm
from apps.tasks.serializers.task import (
    TaskCreateSerializer,
    TaskManageSerializer,
    TaskSerializer,
)
from apps.users.domain.enums.users import UserRole


class TaskViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [JWTAuthentication]

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["category", "education_level", "type", "status"]

    def get_permissions(self):
        if self.action in [
            "create",
            "update",
            "partial_update",
            "my",
            "waiting_accept",
            "submit_for_acceptance",
            "accept",
            "reject",
        ]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = (
            TaskOrm.objects.select_related("category", "created_by")
            .prefetch_related("blocks", "closed_answers")
            .order_by("-created_at")
        )

        if self.action == "my":
            return queryset.filter(created_by=self.request.user)

        if self.action in [
            "waiting_accept",
            "update",
            "partial_update",
            "submit_for_acceptance",
            "accept",
            "reject",
        ]:
            return queryset

        return queryset.filter(status=TaskStatus.ACCEPTED)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TaskCreateSerializer
        if self.action in ["my", "waiting_accept"]:
            return TaskManageSerializer
        return TaskSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action in ["create", "update", "partial_update"]:
            data = kwargs.get("data")
            if data and data.get("payload"):
                payload = json.loads(data["payload"])
                for index, block in enumerate(payload.get("blocks", [])):
                    image = data.get(f"block_images_{index}")
                    if image:
                        block["image"] = image
                for index, answer in enumerate(payload.get("closed_answers", [])):
                    image = data.get(f"closed_answer_images_{index}")
                    if image:
                        answer["image"] = image
                kwargs["data"] = payload

        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role not in [UserRole.ADMIN, UserRole.TEACHER]:
            raise PermissionDenied("Only admins and teachers can create tasks.")

        serializer.save(created_by=user, status=TaskStatus.NEW)

    def perform_update(self, serializer):
        task = self.get_object()

        if task.created_by_id != self.request.user.id:
            raise PermissionDenied("Only task author can edit this task.")

        if task.status != TaskStatus.NEW:
            raise PermissionDenied("Only new tasks can be edited.")

        serializer.save(created_by=self.request.user, status=TaskStatus.NEW)

    @action(detail=False, methods=["get"], url_path="my")
    def my(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="waiting-accept")
    def waiting_accept(self, request):
        if request.user.role != UserRole.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(
            self.get_queryset().filter(status=TaskStatus.WAITING_ACCEPT)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="accept")
    def accept(self, request, pk=None):
        if request.user.role != UserRole.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        task = self.get_object()
        task.status = TaskStatus.ACCEPTED
        task.save(update_fields=["status", "updated_at"])

        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="submit-for-acceptance")
    def submit_for_acceptance(self, request, pk=None):
        task = self.get_object()
        if task.created_by_id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if task.status != TaskStatus.NEW:
            return Response(
                {"detail": "Only new tasks can be submitted for acceptance."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.status = TaskStatus.WAITING_ACCEPT
        task.save(update_fields=["status", "updated_at"])

        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="reject")
    def reject(self, request, pk=None):
        if request.user.role != UserRole.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        task = self.get_object()
        task.status = TaskStatus.REJECTED
        task.save(update_fields=["status", "updated_at"])

        serializer = self.get_serializer(task)
        return Response(serializer.data)
