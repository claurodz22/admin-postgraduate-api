#!/bin/bash

ENV_FILE_PATH="../.env.example"
export $(grep -v '^#' $ENV_FILE_PATH | xargs)

FILENAME="/var/backups/backup.tar"

echo "Backing up database $POSTGRES_DB to $FILENAME..."

docker exec -i postgres-container pg_dump -U $POSTGRES_USER -d $POSTGRES_DB -F t -f $FILENAME
# pg_dump -U $POSTGRES_USER -d $POSTGRES_DB -F c -f $FILENAME
# docker cp postgres-container:/var/lib/postgresql/data/backups/mydb_backup.sql /local/host/backups/
docker cp postgres-container:$FILENAME ./

echo "Backup complete."
