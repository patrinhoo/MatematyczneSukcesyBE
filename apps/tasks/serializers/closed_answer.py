from rest_framework import serializers

from apps.tasks.models.closed_answer_orm import ClosedAnswerOrm


class ClosedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosedAnswerOrm
        exclude = [
            "task",
            "is_correct",
        ]


class ClosedAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosedAnswerOrm
        fields = [
            "order",
            "type",
            "is_correct",
            "content",
            "image",
        ]


class ClosedAnswerManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosedAnswerOrm
        fields = [
            "id",
            "order",
            "type",
            "is_correct",
            "content",
            "image",
        ]
