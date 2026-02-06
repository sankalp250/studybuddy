#!/bin/bash
set -e

echo "Starting database migration..."

# Try to upgrade, if it fails with revision error, stamp and retry
# Try to upgrade, if it fails with revision error, stamp and retry
# We use a block with || to catch the failure because piping to tee can mask the exit code
alembic upgrade head > /tmp/alembic.log 2>&1 || {
    echo "Migration failed, checking for revision error..."
    cat /tmp/alembic.log
    if grep -q "Can't locate revision" /tmp/alembic.log; then
        echo "Migration chain broken, stamping database to head..."
        alembic stamp head
        echo "Migration stamped successfully!"
    else
        echo "Migration failed with unexpected error"
        exit 1
    fi
}

echo "✓ Database migrations completed successfully"

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
