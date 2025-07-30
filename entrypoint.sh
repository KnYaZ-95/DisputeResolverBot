#!/bin/sh
set -e

if [ "$MIGRATIONS" = "true" ]; then
    echo "Running Alembic migrations..."
    alembic upgrade head
fi

exec "$@"
