# CELERY BEAT

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count, Q
from django.template.loader import render_to_string

User = get_user_model()


@shared_task
def send_task_summary_report():
    report = User.objects.annotate(
        yet_to_start=Count("tasks", filter=Q(tasks__status="Yet To Start")),
        in_progress=Count("tasks", filter=Q(tasks__status="In Progress")),
        completed=Count("tasks", filter=Q(tasks__status="Completed")),
        cancelled=Count("tasks", filter=Q(tasks__status="Cancelled")),
        on_hold=Count("tasks", filter=Q(tasks__status="On Hold")),
        under_review=Count("tasks", filter=Q(tasks__status="Under Review")),
        total=Count("tasks"),
    )

    html_content = render_to_string("emails/task/admin_report.html", {"users": report})

    email = EmailMultiAlternatives(
        subject="Task Summary Report",
        body="Task summary report",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=["lokrajkumarv@gmail.com"],
        cc=[
            # "manager@example.com",
            # "lead@example.com"
        ],
        bcc=[
            # "audit@example.com"
        ],
    )

    email.attach_alternative(html_content, "text/html")

    email.send()
