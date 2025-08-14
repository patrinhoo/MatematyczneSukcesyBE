from rest_framework import serializers

from apps.core.serializers.category import CategorySerializer
from apps.tasks.models.task_orm import TaskOrm
from apps.tasks.serializers.closed_answer import ClosedAnswerSerializer
from apps.tasks.serializers.task_block import TaskBlockSerializer
from apps.users.serializers.user import BasicUserInfoSerializer


class TaskSerializer(serializers.ModelSerializer):
    blocks = TaskBlockSerializer(many=True, read_only=True)
    closed_answers = ClosedAnswerSerializer(many=True, read_only=True)
    category = CategorySerializer()
    created_by = BasicUserInfoSerializer()

    class Meta:
        model = TaskOrm
        exclude = [
            "created_at",
            "updated_at",
        ]
