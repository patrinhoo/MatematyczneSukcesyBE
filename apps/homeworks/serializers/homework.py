from rest_framework import serializers

from apps.homeworks.models.homework_orm import HomeworkOrm
from apps.homeworks.serializers.homework_task import HomeworkTaskListSerializer
from apps.users.serializers.user import BasicUserInfoSerializer


class HomeworkSerializer(serializers.ModelSerializer):
    assigned_by = BasicUserInfoSerializer(read_only=True)
    assigned_to = BasicUserInfoSerializer(read_only=True)
    homework_tasks = HomeworkTaskListSerializer(many=True, read_only=True)

    class Meta:
        model = HomeworkOrm
        fields = "__all__"
