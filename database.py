import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_NAME = os.path.join(DATA_DIR, "expense.db")


def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():

    connection = get_db_connection()
    cursor = connection.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Transactions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            transaction_date TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Categories Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_type TEXT NOT NULL,
            category_name TEXT NOT NULL,
            UNIQUE(category_type, category_name)
        )
    """)

    # Budget Table
    # Budget Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            monthly_budget REAL NOT NULL,

            month INTEGER NOT NULL,

            year INTEGER NOT NULL,

            FOREIGN KEY(user_id) REFERENCES users(id),

            UNIQUE(user_id, month, year)
        )
    """)

    # Default Categories
    default_categories = [
        ("Income", "Salary"),
        ("Income", "Freelancing"),
        ("Income", "Business"),
        ("Income", "Investment"),
        ("Income", "Other"),

        ("Expense", "Food"),
        ("Expense", "Travel"),
        ("Expense", "Shopping"),
        ("Expense", "Bills"),
        ("Expense", "Education"),
        ("Expense", "Healthcare"),
        ("Expense", "Entertainment"),
        ("Expense", "Utilities"),
        ("Expense", "Other")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO categories
        (category_type, category_name)
        VALUES (?, ?)
    """, default_categories)

    connection.commit()
    connection.close()