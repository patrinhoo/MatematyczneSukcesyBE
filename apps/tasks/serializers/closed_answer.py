from rest_framework import serializers

from apps.tasks.models.closed_answer_orm import ClosedAnswerOrm


class ClosedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosedAnswerOrm
        exclude = [
            "task",
            "is_correct",
        ]
