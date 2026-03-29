"""
Django settings for the Django Starter project.

This file is intentionally minimal — it contains only what is needed to
run the hello-world endpoint in a containerised environment.

Key design decision — database switching:
    The DB environment variable (read from .env via Docker Compose) drives
    which database backend Django uses at runtime. There is no code change
    required to switch databases; only the .env value and the Compose profile
    need to change. This pattern is called "twelve-factor app" configuration:
    https://12factor.net/config
"""

import os
from pathlib import Path

# ── Path configuration ────────────────────────────────────────────────────────
# BASE_DIR resolves to the "src/" directory — the folder that contains manage.py.
BASE_DIR = Path(__file__).resolve().parent.parent


# ── Security ──────────────────────────────────────────────────────────────────
# SECRET_KEY is used by Django to sign cookies, sessions, and CSRF tokens.
# It MUST be kept secret in production. Here we read it from the environment
# so it never needs to be hard-coded in source code.
SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-dev-key-replace-in-production")

# DEBUG=True enables detailed error pages. Never run with DEBUG=True in production.
DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")

# ALLOWED_HOSTS controls which domain names Django will serve.
# Accepts a comma-separated list from the environment.
_raw_hosts = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]


# ── Installed apps ────────────────────────────────────────────────────────────
# Only the default Django apps are included. No custom app is needed yet —
# the hello-world view lives directly in config/views.py.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core.apps.CoreConfig", 
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# The root URL configuration — Django's routing entry point.
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"


# ── Database configuration ────────────────────────────────────────────────────
# The DB environment variable is the single source of truth for which backend
# to use. The entrypoint.sh script and docker-compose.yml profiles together
# ensure the right service is running before Django starts.
_db_backend = os.environ.get("DB", "sqlite").lower()

if _db_backend == "postgres":
    # PostgreSQL — requires the "db" container to be running (--profile postgres).
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "django_db"),
            "USER": os.environ.get("DB_USER", "django_user"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "django_password"),
            # "db" is the Docker Compose service name — Docker's internal DNS
            # resolves it to the container's IP address automatically.
            "HOST": os.environ.get("DB_HOST", "db"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }

elif _db_backend == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME", "django_db"),
            "USER": os.environ.get("DB_USER", "django_user"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "django_password"),
            # "mysql" é o nome do serviço no docker-compose.yml —
            # o DNS interno do Docker resolve para o IP do container.
            "HOST": os.environ.get("DB_HOST", "mysql"),
            "PORT": os.environ.get("DB_PORT", "3306"),
            "OPTIONS": {
                # Força o charset correto na conexão, independentemente
                # do padrão do servidor MySQL.
                "charset": "utf8mb4",
            },
        }
    }
    
else:
    # SQLite — the default. No external service required.
    # The database file is stored at src/db.sqlite3 inside the container.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            # To pull the SQLite file out of the container for inspection, use:
            # docker compose cp -f web:/app/db.sqlite3 ./docker/sqlite/db.sqlite3
            "NAME": "/app/db.sqlite3",
        }
    }


# ── Password validation ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ── Static files ──────────────────────────────────────────────────────────────
STATIC_URL = "static/"


# ── Default primary key type ──────────────────────────────────────────────────
# BigAutoField uses a 64-bit integer, giving ~9.2 quintillion possible IDs.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
