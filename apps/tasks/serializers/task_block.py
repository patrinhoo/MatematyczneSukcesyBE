from rest_framework import serializers

from apps.tasks.models.task_block_orm import TaskBlockOrm


class TaskBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskBlockOrm
        exclude = [
            "id",
            "task",
        ]


class TaskBlockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskBlockOrm
        fields = [
            "order",
            "type",
            "inline",
            "content",
            "image",
        ]
