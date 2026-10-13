from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "dev-only-webhook-inspector-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "webhook_inspector.urls"
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.staticfiles", "inspector_app"]
MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "inspector.sqlite3"}
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "inspector_app/templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    }
]
STATIC_URL = "static/"
ROOT_TOKEN = "dev-webhook-token"
