import os

from dotenv import load_dotenv

load_dotenv()

env = os.getenv("DJANGO_ENV", "local")

if env == "production":
    from app.settings.production import *  # noqa: F403
else:
    from app.settings.local import *  # noqa: F403
