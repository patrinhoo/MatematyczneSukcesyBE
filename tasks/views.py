from rest_framework import mixins, viewsets

from tasks import models
from tasks import serializers


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
