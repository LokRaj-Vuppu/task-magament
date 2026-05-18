from django.contrib import admin

from reports.models import Report


@admin.register(Report)
class AdminForReports(admin.ModelAdmin):
    readonly_fields = (
        "created_at",
        "updated_at",
        "uuid",
    )
