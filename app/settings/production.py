import os

from app.settings.base import *  # noqa: F403, F405

# from app.settings.base import BASE_DIR

DEBUG = True
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_TASK_ALWAYS_EAGER = False

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": os.getenv("AWS_STORAGE_BUCKET_NAME"),
            "region_name": os.getenv("AWS_S3_REGION_NAME"),
            "location": "media",
            "file_overwrite": False,
            "default_acl": None,
            "querystring_auth": True,
            "signature_version": "s3v4",
            "addressing_style": "virtual",
            "cloudfront_key_id": os.getenv("AWS_CLOUDFRONT_KEY_ID"),
            "cloudfront_key": os.getenv("AWS_CLOUDFRONT_KEY").replace("\\n", "\n"),
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


AWS_QUERYSTRING_EXPIRE = 600
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_REGION_NAME = "ap-south-1"
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")
