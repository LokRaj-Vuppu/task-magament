from rest_framework import serializers

from core.models import Task, TaskPriority, TaskStatus


class TaskSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_uuid = serializers.UUIDField(source="user.uuid", read_only=True)
    task_uuid = serializers.UUIDField(source="uuid", read_only=True)

    class Meta:
        model = Task
        fields = (
            "task_uuid",
            "title",
            "description",
            "priority",
            "status",
            "created_at",
            "updated_at",
            "user_name",
            "user_email",
            "user_uuid",
        )

    def get_user_name(self, obj):
        return f"{obj.user.full_name}"


class CreateTaskRequestValidationSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    priority = serializers.ChoiceField(
        required=False,
        choices=TaskPriority,
        allow_null=True,
        allow_blank=True,
        default=TaskPriority.LOW,
    )
    status = serializers.ChoiceField(
        required=False,
        choices=TaskStatus,
        allow_null=True,
        allow_blank=True,
        default=TaskStatus.YET_TO_START,
    )


class UpdateTaskRequestValidationSerializer(serializers.Serializer):
    task_uuid = serializers.UUIDField(required=True, allow_null=False)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    priority = serializers.ChoiceField(
        required=False, choices=TaskPriority, allow_null=True, allow_blank=True
    )
    status = serializers.ChoiceField(
        required=False, choices=TaskStatus, allow_null=True, allow_blank=True
    )

    def validate(self, attrs):
        update_fields = ["description", "priority", "status"]

        if not any(field in attrs for field in update_fields):
            raise serializers.ValidationError(
                "At least one field (description, priority, status) is required."
            )
        return attrs


class DeleteTaskRequestValidationSerializer(serializers.Serializer):
    task_uuid = serializers.UUIDField(required=True, allow_null=False)
