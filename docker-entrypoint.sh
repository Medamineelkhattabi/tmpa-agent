#!/bin/bash
# Docker entrypoint script for Oracle EBS Assistant

set -e

echo "🚀 Starting Oracle EBS R12 Assistant..."

# Wait for dependencies (if using external services)
if [ "$WAIT_FOR_REDIS" = "true" ]; then
    echo "⏳ Waiting for Redis..."
    while ! nc -z redis 6379; do
        sleep 1
    done
    echo "✅ Redis is ready"
fi

if [ "$WAIT_FOR_POSTGRES" = "true" ]; then
    echo "⏳ Waiting for PostgreSQL..."
    while ! nc -z postgres 5432; do
        sleep 1
    done
    echo "✅ PostgreSQL is ready"
fi

# Run database migrations (if applicable)
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "🔄 Running database migrations..."
    # Add migration commands here when database is implemented
fi

# Start the application
echo "🏢 Oracle EBS R12 Assistant starting on port 8000..."
exec "$@"