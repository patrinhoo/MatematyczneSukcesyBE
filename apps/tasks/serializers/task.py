from rest_framework import serializers

from apps.core.models.category_orm import CategoryOrm
from apps.core.serializers.category import CategorySerializer
from apps.tasks.domain.enums.tasks import TaskType
from apps.tasks.models.closed_answer_orm import ClosedAnswerOrm
from apps.tasks.models.task_block_orm import TaskBlockOrm
from apps.tasks.models.task_orm import TaskOrm
from apps.tasks.serializers.closed_answer import (
    ClosedAnswerCreateSerializer,
    ClosedAnswerManageSerializer,
    ClosedAnswerSerializer,
)
from apps.tasks.serializers.task_block import (
    TaskBlockCreateSerializer,
    TaskBlockSerializer,
)
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


class TaskManageSerializer(TaskSerializer):
    closed_answers = ClosedAnswerManageSerializer(many=True, read_only=True)


class TaskCreateSerializer(serializers.ModelSerializer):
    blocks = TaskBlockCreateSerializer(many=True)
    closed_answers = ClosedAnswerCreateSerializer(many=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryOrm.objects.all())

    class Meta:
        model = TaskOrm
        fields = [
            "id",
            "category",
            "education_level",
            "type",
            "difficulty",
            "blocks",
            "closed_answers",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        blocks = attrs.get("blocks", [])
        closed_answers = attrs.get("closed_answers", [])

        if not blocks:
            raise serializers.ValidationError(
                {"blocks": "Task must contain at least one block."}
            )

        if attrs.get("type") == TaskType.CLOSED and not closed_answers:
            raise serializers.ValidationError(
                {"closed_answers": "Closed task must contain answers."}
            )

        if closed_answers and not any(answer["is_correct"] for answer in closed_answers):
            raise serializers.ValidationError(
                {"closed_answers": "At least one answer must be marked as correct."}
            )

        return attrs

    def create(self, validated_data):
        blocks = validated_data.pop("blocks")
        closed_answers = validated_data.pop("closed_answers", [])
        task = TaskOrm.objects.create(**validated_data)

        self._replace_blocks(task, blocks)
        self._replace_closed_answers(task, closed_answers)

        return task

    def update(self, instance, validated_data):
        blocks = validated_data.pop("blocks")
        closed_answers = validated_data.pop("closed_answers", [])
        existing_blocks = {block.order: block for block in instance.blocks.all()}
        existing_answers = {
            answer.order: answer for answer in instance.closed_answers.all()
        }

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for block in blocks:
            existing_block = existing_blocks.get(block.get("order"))
            if (
                existing_block
                and block.get("type") == existing_block.type
                and existing_block.image
                and not block.get("image")
            ):
                block["image"] = existing_block.image

        for answer in closed_answers:
            existing_answer = existing_answers.get(answer.get("order"))
            if (
                existing_answer
                and answer.get("type") == existing_answer.type
                and existing_answer.image
                and not answer.get("image")
            ):
                answer["image"] = existing_answer.image

        instance.blocks.all().delete()
        instance.closed_answers.all().delete()
        self._replace_blocks(instance, blocks)
        self._replace_closed_answers(instance, closed_answers)

        return instance

    def _replace_blocks(self, task, blocks):
        TaskBlockOrm.objects.bulk_create(
            TaskBlockOrm(task=task, **block) for block in blocks
        )

    def _replace_closed_answers(self, task, closed_answers):
        ClosedAnswerOrm.objects.bulk_create(
            ClosedAnswerOrm(task=task, **answer) for answer in closed_answers
        )
