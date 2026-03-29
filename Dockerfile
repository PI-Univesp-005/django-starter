# ─────────────────────────────────────────────────────────────────────────────
# Base image: Python 3.13 slim (Debian-based, minimal footprint)
# Django 5.2 LTS officially supports Python 3.10 – 3.14.
# The slim variant keeps the image small; we install only what we need.
# SQLite 3.46.x is bundled with this Python image — no separate installation.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.13-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
# so container logs appear immediately instead of being buffered.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System-level build dependencies needed to compile psycopg2 if ever needed,
# plus curl (health-check / debugging), and postgresql-client (pg_isready).
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        postgresql-client \
        default-libmysqlclient-dev \
        pkg-config \
        curl \
    && rm -rf /var/lib/apt/lists/*

# All application code lives under /app.
WORKDIR /app

# Copy dependency manifest first. Because Docker caches layers, this means
# pip install only re-runs when requirements.txt actually changes.
COPY requirements.txt ./

# Copy the Django source tree.
COPY src/ ./src

# Copy the entrypoint script and make it executable.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 3333 — the Django development server's default port.
EXPOSE 3333

# The entrypoint handles venv creation, dependency installation,
# optional postgres health-wait, migration, and finally server start.
ENTRYPOINT ["/entrypoint.sh"]
