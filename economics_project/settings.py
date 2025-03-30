import dj_database_url
import socket
import os
from os import listdir
from os.path import (
    basename,
    normpath,
)
from pathlib import Path
from sys import argv
from decouple import config

# LOGGING
from economics_project.logging import *

# AWS
from economics_project.aws import *

# admins
ADMINS = [("bllendev", "bllendev@gmail.com")]  # TODO: add secret
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config("SECRET_KEY", default="fake_test_key")
ENVIRONMENT = config("ENVIRONMENT", default="development")
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "economics-project.herokuapp.com",
]
DEBUG = bool(config("DEBUG", default=False))


TESTING = False
if "test" in argv or "test_coverage" in argv:
    TESTING = True


# stripe
# STRIPE_LIVE_PUBLISHABLE_KEY = config("STRIPE_LIVE_PUBLISHABLE_KEY")
# STRIPE_LIVE_SECRET_KEY = config("STRIPE_LIVE_SECRET_KEY")

# production
if ENVIRONMENT == "production":
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # new

# Application definition
EXCLUDED_APP_DIRECTORIES = [
    "static",
    ".vscode",
    "cover",
    "media",
    "staticfiles",
    "templates",
    "fixtures",
    ".git",
    ".idea",
    ".local",
    "venv",
]
APP_DIRECTORIES_ABSOLUTE = [
    dir_ref for dir_ref in listdir(BASE_DIR) if Path(dir_ref).is_dir()
]
APP_DIRECTORIES_NAMES = [
    basename(normpath(dir_ref)) for dir_ref in APP_DIRECTORIES_ABSOLUTE
]
APP_DIRECTORIES = [
    dir_ref
    for dir_ref in APP_DIRECTORIES_NAMES
    if dir_ref not in EXCLUDED_APP_DIRECTORIES
]
APP_DIRECTORIES_COMMA_LIST = ",".join(APP_DIRECTORIES)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third-Party
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Local
    "common",
    "users",
    "ai",
    "dashboard",
    # "django_celery_beat",  task scheduler
]  # + APP_DIRECTORIES


SITE_ID = 1
ROOT_URLCONF = "economics_project.urls"
WSGI_APPLICATION = "economics_project.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DEFAULT_FROM_EMAIL = "noreply@gmail.com"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASS")
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "home"

ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_REDIRECT = "home"
ACCOUNT_SIGNUP_FIELDS = ["email", "username*", "password1*", "password2*"]
ACCOUNT_UNIQUE_EMAIL = True

MEDIA_URL = "/media/"  # new
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # new
MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
]
if DEBUG:
    MIDDLEWARE.append("django.middleware.cache.FetchFromCacheMiddleware")


hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
# INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
INTERNAL_IPS = [
    "127.0.0.1",
]


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 604800
CACHE_MIDDLEWARE_KEY_PREFIX = ""

# Static files (CSS, JavaScript, Images)
# Cloudinary stuff
CLOUDINARY_STORAGE = {  # TODO: add these to env vars
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

if ENVIRONMENT == "development":
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
else:
    # Cloudinary settings for production
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            BASE_DIR, "db.sqlite3"
        ),  # BASE_DIR should be defined in your settings as the root project directory
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "postgres",
#         "USER": "postgres",
#         "PASSWORD": "postgres",
#         "HOST": config("DB_HOST", "db"),
#         "PORT": config("DB_PORT", "5432"),
#     }
# }

# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES["default"].update(db_from_env)


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
