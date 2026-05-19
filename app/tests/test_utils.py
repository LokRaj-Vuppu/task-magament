from unittest.mock import patch

from app.utils.email_service import EmailService


class TestEmailService:
    @patch("app.utils.email_service.send_email_task.delay")
    @patch("app.utils.email_service.render_to_string")
    def test_send_email_success(self, mock_render, mock_delay):
        mock_render.return_value = "<h1>Hello</h1>"

        EmailService.send(
            subject="Welcome",
            recipient="test@example.com",
            template_name="emails/test.html",
            context={"name": "Jane Smith"},
        )

        mock_render.assert_called_once_with("emails/test.html", {"name": "Jane Smith"})

        mock_delay.assert_called_once_with(
            subject="Welcome",
            html_content="<h1>Hello</h1>",
            recipient="test@example.com",
        )

    @patch("app.utils.email_service.send_email_task.delay")
    @patch("app.utils.email_service.render_to_string")
    def test_send_email_without_context(self, mock_render, mock_delay):
        mock_render.return_value = "<h1>Hello</h1>"

        EmailService.send(
            subject="Welcome",
            recipient="test@example.com",
            template_name="emails/test.html",
        )

        mock_render.assert_called_once_with("emails/test.html", {})

        mock_delay.assert_called_once()

    @patch("app.utils.email_service.send_email_task.delay")
    @patch("app.utils.email_service.render_to_string")
    def test_send_email_template_rendering(self, mock_render, mock_delay):
        mock_render.return_value = "<p>Rendered Template</p>"

        EmailService.send(
            subject="Test",
            recipient="abc@test.com",
            template_name="emails/demo.html",
            context={"x": 1},
        )

        mock_delay.assert_called_once_with(
            subject="Test",
            html_content="<p>Rendered Template</p>",
            recipient="abc@test.com",
        )
