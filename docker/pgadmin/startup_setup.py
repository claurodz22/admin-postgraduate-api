import os
from pgadmin.utils.driver import get_driver

# Initialize the pgAdmin app
app = None
with app.app_context():
    manager = get_driver("PG_DEFAULT").connection_manager
    manager.add_connection(
        {
            "name": "PostgreSQL",
            "host": "postgres",
            "port": 5432,
            "username": "postgres",
            "sslmode": "prefer",
        }
    )
