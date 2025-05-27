from rest_framework import serializers
from django.utils import timezone

from apps.homeworks import models
from apps.tasks import serializers as tasks_serializers
from apps.users import serializers as users_serializers


class HomeworkTaskSerializer(serializers.ModelSerializer):
    task = tasks_serializers.TaskSerializer(read_only=True)

    class Meta:
        model = models.HomeworkTask
        fields = "__all__"


class HomeworkTaskListSerializer(serializers.ModelSerializer):
    task = tasks_serializers.TaskSerializer(read_only=True)

    class Meta:
        model = models.HomeworkTask
        exclude = ["homework"]


class HomeworkTaskSolutionUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HomeworkTask
        fields = ["solution_file"]

    def validate(self, attrs):
        if "solution_file" not in self.initial_data:
            raise serializers.ValidationError(
                {"solution_file": "To pole jest wymagane przy przesyłaniu rozwiązania."}
            )
        return attrs

    def update(self, instance: models.HomeworkTask, validated_data: dict):
        instance.solution_file = validated_data["solution_file"]
        instance.submitted_at = timezone.now()
        instance.save()

        return instance


class HomeworkSerializer(serializers.ModelSerializer):
    assigned_by = users_serializers.BasicUserInfoSerializer(read_only=True)
    assigned_to = users_serializers.BasicUserInfoSerializer(read_only=True)
    homework_tasks = HomeworkTaskListSerializer(many=True, read_only=True)

    class Meta:
        model = models.Homework
        fields = "__all__"
