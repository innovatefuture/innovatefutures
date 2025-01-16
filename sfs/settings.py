import os
import sys
from pathlib import Path

from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent
DJANGO_APPS_DIR = Path(BASE_DIR) / "apps"

# add apps/ to the Python path
sys.path.append(str(DJANGO_APPS_DIR))

SECRET_KEY = os.environ.get("SECRET_KEY", "default-insecure-key-ov6&0l@xp6up")

# default False in case app is deployed without any env variables
DEBUG = True if os.environ.get("DEBUG") == "1" else False

ALLOWED_HOSTS = os.environ.get("DOMAIN_NAME", "sharedfutures.com").split(",")
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    INTERNAL_IPS = [
        # see https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#toolbar-options
        "0.0.0.0",
    ]
    DEBUG_TOOLBAR_CONFIG = {
        # see https://django-debug-toolbar.readthedocs.io/en/latest/tips.html#id1
        "ROOT_TAG_EXTRA_ATTRS": "hx-preserve"
    }

DJANGO_VITE_DEV_MODE = False
if os.environ.get("DJANGO_VITE_DEV_MODE", "") == "1":
    DJANGO_VITE_DEV_MODE = True


# Application definition

INSTALLED_APPS = [
    "django_vite",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.modeladmin",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtailgeowidget",
    "modelcluster",
    "taggit",
    "django.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django_extensions",
    "landing",
    "dashboard",
    "analytics",
    "area",
    "userauth",
    "messaging",
    "action",
    "river",
    "remix",
    "resources",
    "search",
    "spring",
    "core",
    "poll",
    "task",
    "map",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_browser_reload",
    "widget_tweaks",
    "django_htmx",
    "allauth.socialaccount.providers.google",
]
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "analytics.middleware.log_visit_middleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]
if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

ROOT_URLCONF = "sfs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates/userauth"),
            os.path.join(BASE_DIR, "templates/river"),
        ],
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

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "sfs.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": os.environ.get("POSTGRES_HOST"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ: bool = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# must correspond to build.outDir in your ViteJS configuration
DJANGO_VITE_ASSETS_PATH = os.path.join(BASE_DIR, "sfs/vite-build")

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "sfs/static"),
    DJANGO_VITE_ASSETS_PATH,
]

# Account
ACCOUNT_FORMS = {"signup": "userauth.forms.CustomSignupForm"}
# ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Wagtail
WAGTAIL_SITE_NAME = "sfs"
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = os.environ.get("BASE_URL", "https://sharedfutures.space")
CSRF_TRUSTED_ORIGINS = os.environ.get("BASE_URL", "https://sharedfutures.space").split(
    ","
)

# for @login_required
LOGIN_URL = "/profile/login/"

WAGTAIL_USER_EDIT_FORM = "userauth.forms.CustomUserEditForm"
WAGTAIL_USER_CREATION_FORM = "userauth.forms.CustomUserCreationForm"
WAGTAIL_USER_CUSTOM_FIELDS = ["display_name", "year_of_birth", "post_code"]

APPEND_SLASH = True
WAGTAIL_APPEND_SLASH = True

TAGGIT_CASE_INSENSITIVE = True

# celery

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULE = {
    "send_daily_messages": {
        "task": "userauth.tasks.send_daily_messages",
        "schedule": crontab(hour=23, minute=0),
    },
}

# pickle required to serialize and send EmailMultiAlternatives
# https://docs.celeryproject.org/en/latest/userguide/calling.html#calling-serializers
CELERY_ACCEPT_CONTENT = ["pickle"]
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"

# site framework
SITE_ID = 1
SITE_DOMAIN = os.environ.get("BASE_URL", "https://sharedfutures.space")

# allauth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET", "")
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {"client_id": GOOGLE_CLIENT_ID, "secret": GOOGLE_SECRET, "key": ""}
    },
}

ENABLE_ALLAUTH_SOCIAL_LOGIN = False
if os.environ.get("ENABLE_ALLAUTH_SOCIAL_LOGIN", "") == "1":
    ENABLE_ALLAUTH_SOCIAL_LOGIN = True

LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "/dashboard/"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_REQUIRED = False

# needed for oauth
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# custom user model
AUTH_USER_MODEL = "userauth.CustomUser"

# overriding default account
ADAPTER = "userauth.views.CustomAllauthAdapter"
ACCOUNT_ADAPTER = "userauth.views.CustomAllauthAdapter"
SOCIALACCOUNT_ADAPTER = "userauth.adapters.CustomSocialAccountAdapter"

# email
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
if not EMAIL_HOST and not EMAIL_HOST_USER and not EMAIL_HOST_PASSWORD:
    # if email hasn't been set, then enable console backend
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

MAPTILER_API_KEY = os.environ.get("MAPTILER_API_KEY", "NOT SET")

# This is for the wagtail location editor widget
GEO_WIDGET_EMPTY_LOCATION = True
GEO_WIDGET_DEFAULT_LOCATION = {
    # Belfast
    "lat": 54.5996,
    "lng": -5.9213,
}
GEO_WIDGET_ZOOM = 14


if not DEBUG:
    # Logging configuration
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file": {
                "level": "INFO",  # Set to 'ERROR' for less verbose logging
                "class": "logging.FileHandler",
                "filename": "/home/app/sfs/logs/django.log",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": "INFO",  # Set to 'ERROR' for less verbose logging
                "propagate": True,
            },
        },
    }
