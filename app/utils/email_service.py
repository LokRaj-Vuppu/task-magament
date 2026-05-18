from django.template.loader import render_to_string

from app.tasks import send_email_task


class EmailService:
    @staticmethod
    def send(subject, recipient, template_name, context=None):
        context = context or {}

        html_content = render_to_string(template_name, context)

        send_email_task.delay(
            subject=subject, html_content=html_content, recipient=recipient
        )
