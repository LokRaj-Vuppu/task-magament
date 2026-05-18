import uuid

from django.db import models

from accounts.models import TimeStampsForModels, User


class Report(TimeStampsForModels):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    report_name = models.CharField(max_length=255)
    s3_url = models.URLField()
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reports"
        ordering = ["-generated_at"]

    def __str__(self):
        return self.report_name


# Task Summary Report
# Date: 17-May-2026
# User: lokraj@example.com

# -------------------------------------

# Total Tasks: 10
# Completed Tasks: 6
# Pending Tasks: 4

# -------------------------------------

# Task Details

# 1. Learn Docker
#    Priority: High
#    Status: Completed

# 2. Deploy Django on EC2
#    Priority: Medium
#    Status: Pending

# 3. Learn ECS
#    Priority: High
#    Status: Completed

# 4. Setup Redis Cache
#    Priority: Low
#    Status: Pending

# -------------------------------------

# Completion Rate: 60%
