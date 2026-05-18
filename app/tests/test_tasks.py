from unittest.mock import MagicMock, patch

import pytest
from celery.exceptions import Retry
from django.conf import settings

from app.tasks import send_email_task


class TestSendEmailTask:
    @patch("app.tasks.EmailMultiAlternatives")
    def test_send_email_success(self, mock_email_class):
        mock_email = MagicMock()

        mock_email_class.return_value = mock_email

        result = send_email_task.run(
            subject="Welcome",
            html_content="<h1>Hello</h1>",
            recipient="test@example.com",
        )

        mock_email_class.assert_called_once_with(
            subject="Welcome",
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["test@example.com"],
        )

        mock_email.attach_alternative.assert_called_once_with(
            "<h1>Hello</h1>", "text/html"
        )

        mock_email.send.assert_called_once()

        assert result == "Email sent successfully"

    @patch("app.tasks.send_email_task.retry")
    @patch("app.tasks.EmailMultiAlternatives")
    def test_send_email_retry_on_failure(self, mock_email_class, mock_retry):
        mock_email = MagicMock()

        mock_email.send.side_effect = Exception("SMTP Error")

        mock_email_class.return_value = mock_email

        mock_retry.side_effect = Retry()

        with pytest.raises(Retry):
            send_email_task.run(
                subject="Welcome",
                html_content="<h1>Hello</h1>",
                recipient="test@example.com",
            )

        mock_retry.assert_called_once()

    @patch("app.tasks.EmailMultiAlternatives")
    def test_html_content_attached(self, mock_email_class):
        mock_email = MagicMock()

        mock_email_class.return_value = mock_email

        send_email_task.run(
            subject="Test", html_content="<p>Hello</p>", recipient="test@example.com"
        )

        mock_email.attach_alternative.assert_called_once_with(
            "<p>Hello</p>", "text/html"
        )
