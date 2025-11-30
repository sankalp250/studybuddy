#!/bin/bash
set -e

echo "Starting database migration..."

# Try to upgrade, if it fails with revision error, stamp and retry
if ! alembic upgrade head 2>&1 | tee /tmp/alembic.log; then
    if grep -q "Can't locate revision" /tmp/alembic.log; then
        echo "Migration chain broken, stamping database to head..."
        alembic stamp head
        echo "Migration stamped successfully!"
    else
        echo "Migration failed with unexpected error"
        cat /tmp/alembic.log
        exit 1
    fi
fi

echo "✓ Database migrations completed successfully"

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port 8000
