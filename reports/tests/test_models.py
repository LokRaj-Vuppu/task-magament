import pytest

from accounts.models import User
from reports.models import Report


@pytest.mark.django_db
class TestReportModel:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="test@example.com", password="password123", full_name="Jane Smith"
        )

    def test_create_report(self, user):
        report = Report.objects.create(
            user=user,
            report_name="Task Summary Report",
            s3_url="https://bucket.s3.amazonaws.com/report.pdf",
        )

        assert report.id is not None
        assert report.user == user

        assert report.report_name == "Task Summary Report"

        assert report.s3_url == "https://bucket.s3.amazonaws.com/report.pdf"

    def test_uuid_generated(self, user):
        report = Report.objects.create(
            user=user,
            report_name="Task Summary Report",
            s3_url="https://bucket.s3.amazonaws.com/report.pdf",
        )

        assert report.uuid is not None

    def test_generated_at_created(self, user):
        report = Report.objects.create(
            user=user,
            report_name="Task Summary Report",
            s3_url="https://bucket.s3.amazonaws.com/report.pdf",
        )

        assert report.generated_at is not None

    def test_string_representation(self, user):
        report = Report.objects.create(
            user=user,
            report_name="Task Summary Report",
            s3_url="https://bucket.s3.amazonaws.com/report.pdf",
        )

        assert str(report) == "Task Summary Report"

    def test_report_ordering(self, user):
        report1 = Report.objects.create(
            user=user,
            report_name="Report1",
            s3_url="https://bucket.s3.amazonaws.com/report1.pdf",
        )

        report2 = Report.objects.create(
            user=user,
            report_name="Report2",
            s3_url="https://bucket.s3.amazonaws.com/report2.pdf",
        )

        reports = Report.objects.all()

        # latest first because:
        # ordering=["-generated_at"]

        assert reports[0] == report2
        assert reports[1] == report1

    def test_delete_user_deletes_reports(self, user):
        report = Report.objects.create(
            user=user,
            report_name="Task Summary Report",
            s3_url="https://bucket.s3.amazonaws.com/report.pdf",
        )

        user.delete()

        assert Report.objects.filter(id=report.id).count() == 0
