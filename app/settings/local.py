import os

from app.settings.base import *  # noqa: F403, F405

# from app.settings.base import BASE_DIR  #F401

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "task_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:8000")

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//"
)
CELERY_TASK_ALWAYS_EAGER = os.getenv("CELERY_TASK_ALWAYS_EAGER", "False") == "True"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
