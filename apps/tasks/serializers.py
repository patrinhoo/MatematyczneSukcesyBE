from rest_framework import serializers

from apps.tasks import models
from apps.core import serializers as core_serializers
from apps.users import serializers as users_serializers


class TaskBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskBlock
        exclude = [
            "id",
            "task",
        ]


class ClosedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClosedAnswer
        exclude = [
            "task",
            "is_correct",
        ]


class TaskSerializer(serializers.ModelSerializer):
    blocks = TaskBlockSerializer(many=True, read_only=True)
    closed_answers = ClosedAnswerSerializer(many=True, read_only=True)
    category = core_serializers.CategorySerializer()
    created_by = users_serializers.BasicUserInfoSerializer()

    class Meta:
        model = models.Task
        exclude = [
            "created_at",
            "updated_at",
        ]
