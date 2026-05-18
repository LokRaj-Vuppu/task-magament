from django.contrib import admin

from accounts.models import User

# admin.site.register(TaskResult)


@admin.register(User)
class AdminForUser(admin.ModelAdmin):
    readonly_fields = (
        "created_at",
        "updated_at",
        "uuid",
    )
