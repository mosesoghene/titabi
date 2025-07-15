import time
import psycopg2
from psycopg2 import OperationalError
import os


def wait_for_postgres():
    db_name = os.getenv("POSTGRES_DB", "postgres")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", 5432)

    print(f"⏳ Waiting for PostgreSQL at {db_host}:{db_port}...")

    while True:
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            conn.close()
            print("✅ PostgreSQL is ready!")
            break
        except OperationalError:
            print("❌ PostgreSQL not available yet. Retrying in 1s...")
            time.sleep(1)


if __name__ == "__main__":
    wait_for_postgres()
