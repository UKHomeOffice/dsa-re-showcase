import psycopg2
import os
from otel_config import meter

# Database connection details
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    return conn

# Initialize the database table
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_counts (
            id SERIAL PRIMARY KEY,
            total_count INT NOT NULL
        );
    """)
    cursor.execute("""
        INSERT INTO login_counts (total_count)
        SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM login_counts);
    """)
    conn.commit()
    cursor.close()
    conn.close()

def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_counts;")
        rows = cursor.fetchall()
        print("Database connection successful. Rows in login_counts table:")
        for row in rows:
            print(row)
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

# Create a counter for login events
db_login_event_counter = meter.create_up_down_counter(
    name="db_login_event_counter",
    description="Counts the number of login events processed in the deployed database",
    unit="1"
)

# Fetch the total_count from the database and update the counter
def update_db_login_event_counter():
    """Fetch the total_count from the database and update the counter."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT total_count FROM login_counts WHERE id = 1;")
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            total_count = result[0]
            # Update the OpenTelemetry counter
            db_login_event_counter.add(total_count, {"db.table": "login_counts", "operation": "fetch"})
            print(f"Updated db_login_event_counter to {total_count}.")
        else:
            print("No total_count found in the database.")
    except Exception as e:
        print(f"Error updating db_login_event_counter: {e}")