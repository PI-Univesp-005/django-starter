#!/bin/bash
set -e

VENV_DIR="/app/.venv"
PFX="⚙️  [\033[3mentrypoint.sh\033[0m]:"

# ── Step 1: Virtual environment ───────────────────────────────────────────────
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    printf "$PFX 🐍 \033[1mCreating virtual environment at $VENV_DIR ...\033[0m\n"
    python -m venv "$VENV_DIR"
    printf "$PFX ✅ \033[1mVirtual environment created.\033[0m\n"
else
    printf "$PFX ✅ \033[1mVirtual environment already exists.\033[0m\n"
fi

# ── Step 2: Dependencies ──────────────────────────────────────────────────────
printf "$PFX 📦 \033[1mInstalling / verifying Python dependencies ...\033[0m\n"
source "$VENV_DIR/bin/activate"
pip install --quiet --upgrade pip
# /requirements.txt is outside /app so the volume mount cannot shadow it
pip install --quiet -r requirements.txt
printf "$PFX ✅ \033[1mDependencies up to date.\033[0m\n"

# ── Step 3: Wait for the database ────────────────────────────────────────────
DB="${DB:-sqlite}"
PORT="${PORT:-3333}"

if [ "$DB" = "postgres" ]; then
    printf "$PFX 🐘 \033[1mDB=postgres — waiting for PostgreSQL...\033[0m\n"
    MAX_RETRIES=30
    RETRY_INTERVAL=2
    attempt=0

    until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres_db'),
        port=int(os.getenv('DB_PORT', 5432)),
        dbname=os.getenv('DB_NAME', 'django_db'),
        user=os.getenv('DB_USER', 'django_user'),
        password=os.getenv('DB_PASSWORD', 'django_password'),
    )
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
        attempt=$(( attempt + 1 ))
        if [ "$attempt" -ge "$MAX_RETRIES" ]; then
            printf "$PFX ❌ \033[1mPostgreSQL did not become ready. Aborting.\033[0m\n"
            exit 1
        fi
        printf "$PFX   \033[1m Attempt $attempt/$MAX_RETRIES — retrying in ${RETRY_INTERVAL}s...\033[0m\n"
        sleep "$RETRY_INTERVAL"
    done
    printf "$PFX ✅ \033[1mPostgreSQL is ready.\033[0m\n"

elif [ "$DB" = "mysql" ]; then
    printf "$PFX 🐬 \033[1mDB=mysql — waiting for MySQL...\033[0m\n"
    MAX_RETRIES=30
    RETRY_INTERVAL=2
    attempt=0

    until python -c "
import MySQLdb, os, sys
try:
    MySQLdb.connect(
        host=os.getenv('DB_HOST', 'mysql'),
        port=int(os.getenv('DB_PORT', 3306)),
        db=os.getenv('DB_NAME', 'django_db'),
        user=os.getenv('DB_USER', 'django_user'),
        passwd=os.getenv('DB_PASSWORD', 'django_password'),
    )
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
        attempt=$(( attempt + 1 ))
        if [ "$attempt" -ge "$MAX_RETRIES" ]; then
            printf "$PFX ❌ \033[1mMySQL did not become ready. Aborting.\033[0m\n"
            exit 1
        fi
        printf "$PFX   \033[1m Attempt $attempt/$MAX_RETRIES — retrying in ${RETRY_INTERVAL}s...\033[0m\n"
        sleep "$RETRY_INTERVAL"
    done
    printf "$PFX ✅ \033[1mMySQL is ready.\033[0m\n"

else
    printf "$PFX 🗄️ \033[1m DB=sqlite — no external service to wait for.\033[0m\n"
fi

# ── Step 4: Migrate, load fixtures and serve ─────────────────────────────────────────────────
printf "$PFX 🔄 \033[1mRunning database migrations ...\033[0m\n"

python scripts/manage.py migrate --noinput
if [ "$ENV" != "production" ]; then
    printf "\n$PFX 🔍 \033[1mChecking database state ...\033[0m\n"
    # Executa o check em uma única linha para evitar IndentationError
    # Usa get_user_model() para prevenir crash caso exista um Custom User Model
    if python scripts/manage.py shell -c "import sys; from django.contrib.auth import get_user_model; sys.exit(1 if get_user_model().objects.exists() else 0)" > /dev/null 2>&1; then
        printf "$PFX 🌱 \033[1mDatabase is fresh. Loading initial data fixtures ...\033[0m\n\t  "
        python scripts/manage.py loaddata /app/fixtures/initial_data.json
    else
        printf "$PFX ⚠️  \033[1mDatabase already populated. Skipping fixtures.\033[0m\n"
    fi
fi

printf "$PFX 🚀 \033[1mDjango development server has started on\033[0m http://0.0.0.0:$PORT\n"
printf "$PFX 🛢️  \033[1mDatabase backend:\033[0m $DB\n"
printf "\n"

exec python scripts/manage.py runserver 0.0.0.0:$PORT 1> /dev/null