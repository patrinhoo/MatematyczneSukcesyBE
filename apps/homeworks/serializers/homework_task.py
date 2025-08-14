from rest_framework import serializers
from django.utils import timezone

from apps.homeworks.models.homework_task_orm import HomeworkTaskOrm
from apps.tasks.serializers.task import TaskSerializer


class HomeworkTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = HomeworkTaskOrm
        fields = "__all__"


class HomeworkTaskListSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = HomeworkTaskOrm
        exclude = ["homework"]


class HomeworkTaskSolutionUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkTaskOrm
        fields = ["solution_file"]

    def validate(self, attrs):
        if "solution_file" not in self.initial_data:
            raise serializers.ValidationError(
                {"solution_file": "To pole jest wymagane przy przesyłaniu rozwiązania."}
            )
        return attrs

    def update(self, instance: HomeworkTaskOrm, validated_data: dict):
        instance.solution_file = validated_data["solution_file"]
        instance.submitted_at = timezone.now()
        instance.save()

        return instance
