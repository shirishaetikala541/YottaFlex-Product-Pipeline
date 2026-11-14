import sqlite3
import os


DB_PATH = "data/product_pipeline.db"


def get_connection():
    os.makedirs("data", exist_ok=True)

    return sqlite3.connect(DB_PATH)


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            price REAL,
            stock_quantity INTEGER,
            source_supplier TEXT,
            source_file TEXT
        )
        """
    )

    connection.commit()
    connection.close()