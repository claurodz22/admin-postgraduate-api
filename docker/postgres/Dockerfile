FROM postgres:latest

# Set environment variables for PostgreSQL
# ENV POSTGRES_DB=your_database
# ENV POSTGRES_USER=postgres
# ENV POSTGRES_PASSWORD=your_password
# ENV POSTGRES_PASSWORD="postgres"
# ENV POSTGRES_USER="postgres"
# ENV POSTGRES_HOST="127.0.0.1"
# ENV POSTGRES_DB="udo_test_db"

# Copy the backup file into the container
COPY backup.tar /docker-entrypoint-initdb.d/backup.tar

# Add a script to restore the database
COPY restore.sh /docker-entrypoint-initdb.d/restore.sh
RUN chmod +x /docker-entrypoint-initdb.d/restore.sh
