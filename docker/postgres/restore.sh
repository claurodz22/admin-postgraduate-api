#!/bin/bash
set -e

echo "Restoring database from backup.tar..."
pg_restore --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --no-password /docker-entrypoint-initdb.d/backup.tar
echo "Database restoration complete."
