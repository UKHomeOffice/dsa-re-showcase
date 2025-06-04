import psycopg2
import os

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

from db import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_counts;")
    rows = cursor.fetchall()
    print("Database is working. Rows in login_counts table:")
    for row in rows:
        print(row)
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")