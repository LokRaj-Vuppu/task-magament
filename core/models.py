import uuid

from django.db import models

from accounts.models import TimeStampsForModels, User


class TaskPriority(models.TextChoices):
    LOW = "Low", "Low"
    MEDIUM = "Medium", "Medium"
    HIGH = "High", "High"


class TaskStatus(models.TextChoices):
    YET_TO_START = "Yet To Start", "Yet To Start"
    IN_PROGRESS = "In Progress", "In Progress"
    ON_HOLD = (
        "On Hold",
        "On Hold",
    )
    UNDER_REVIEW = "Under Review", "Under Review"
    CANCELLED = "Cancelled", "Cancelled"
    COMPLETED = "Completed", "Completed"


class Task(TimeStampsForModels):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(
        max_length=20, choices=TaskPriority.choices, default=TaskPriority.LOW
    )
    status = models.CharField(
        max_length=20, choices=TaskStatus.choices, default=TaskStatus.YET_TO_START
    )

    class Meta:
        db_table = "tasks"

    def __str__(self):
        return f"{self.user.full_name} | {self.title} | {self.priority} | {self.status}"


class TaskAttachment(TimeStampsForModels):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="task_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_attachments"

    def __str__(self):
        return f"{self.task.user.full_name} | {self.file.name}"
