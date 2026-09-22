"""Database connection configuration.

SEEDED ISSUE (security, blocking):
The password below is hardcoded in source instead of being pulled from an
environment variable / secrets manager. The Security subagent should flag
this as a blocking finding.
"""

import psycopg2


DB_HOST = "prod-db.internal.example.com"
DB_USER = "app_service"
DB_PASSWORD = "SuperSecret123!"  # <-- seeded issue: hardcoded credential
DB_NAME = "app_production"


def get_connection():
    """Open a connection to the production database."""
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
    )
