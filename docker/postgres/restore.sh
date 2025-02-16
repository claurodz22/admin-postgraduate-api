#!/bin/bash
# set -e
ENV_FILE_PATH="../.env.example"
export $(grep -v '^#' $ENV_FILE_PATH | xargs)

FILENAME="/var/backups/backup.tar"

echo "Restoring database from backup.tar..."
docker exec -i postgres-container pg_restore --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --no-password --clean --if-exists /docker-entrypoint-initdb.d/backup.tar
echo "Database restoration complete."
