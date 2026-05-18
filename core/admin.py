from django.contrib import admin

from core.models import Task, TaskAttachment


@admin.register(Task)
class AdminForTask(admin.ModelAdmin):
    readonly_fields = (
        "created_at",
        "updated_at",
        "uuid",
    )


@admin.register(TaskAttachment)
class AdminForTaskAttachment(admin.ModelAdmin):
    readonly_fields = (
        "created_at",
        "updated_at",
        "uuid",
    )
