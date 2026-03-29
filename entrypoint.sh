#!/bin/bash
set -e

VENV_DIR="/app/.venv"

# ── Step 1: Virtual environment ───────────────────────────────────────────────
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "🐍 Creating virtual environment at $VENV_DIR ..."
    python -m venv "$VENV_DIR"
    echo "✅ Virtual environment created."
else
    echo "✅ Virtual environment already exists."
fi

# ── Step 2: Dependencies ──────────────────────────────────────────────────────
echo "📦 Installing / verifying Python dependencies ..."
source "$VENV_DIR/bin/activate"
pip install --quiet --upgrade pip
# /requirements.txt is outside /app so the volume mount cannot shadow it
pip install --quiet -r requirements.txt
echo "✅ Dependencies up to date."

# ── Step 3: Wait for the database ────────────────────────────────────────────
DB="${DB:-sqlite}"

if [ "$DB" = "postgres" ]; then
    echo "🐘 DB=postgres — waiting for PostgreSQL..."
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
            echo "❌ PostgreSQL did not become ready. Aborting."
            exit 1
        fi
        echo "   Attempt $attempt/$MAX_RETRIES — retrying in ${RETRY_INTERVAL}s..."
        sleep "$RETRY_INTERVAL"
    done
    echo "✅ PostgreSQL is ready."

elif [ "$DB" = "mysql" ]; then
    echo "🐬 DB=mysql — waiting for MySQL..."
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
            echo "❌ MySQL did not become ready. Aborting."
            exit 1
        fi
        echo "   Attempt $attempt/$MAX_RETRIES — retrying in ${RETRY_INTERVAL}s..."
        sleep "$RETRY_INTERVAL"
    done
    echo "✅ MySQL is ready."

else
    echo "🗄️  DB=sqlite — no external service to wait for."
fi

# ── Step 4: Migrate and serve ─────────────────────────────────────────────────
echo "🔄 Running database migrations ..."
python src/manage.py migrate --noinput

echo ""
echo "🚀 Starting Django development server on http://0.0.0.0:8000 ..."
echo "   Database backend: $DB"
echo ""

exec python src/manage.py runserver 0.0.0.0:8000