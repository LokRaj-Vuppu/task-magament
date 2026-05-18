from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


@shared_task(bind=True, max_retries=3)
def send_email_task(self, subject, html_content, recipient):
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )

        email.attach_alternative(html_content, "text/html")

        email.send()

        return "Email sent successfully"
    except Exception as e:
        raise self.retry(exc=e, countdown=60) from e
