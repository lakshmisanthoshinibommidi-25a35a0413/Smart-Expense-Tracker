import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_NAME = os.path.join(DATA_DIR, "expense.db")

class PostgresCursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        # 1. Translate placeholders from SQLite (?) to PostgreSQL (%s)
        query = query.replace('?', '%s')
        
        # 2. Translate SQLite-specific AUTOINCREMENT to PostgreSQL SERIAL
        query = query.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
        
        # 3. Translate SQLite INSERT OR IGNORE to PostgreSQL INSERT ... ON CONFLICT DO NOTHING
        query = query.replace('INSERT OR IGNORE', 'INSERT')
        if 'INSERT INTO categories' in query and 'ON CONFLICT' not in query:
            query = query + ' ON CONFLICT DO NOTHING'
        if 'INSERT INTO budgets' in query and 'ON CONFLICT' not in query:
            query = query + ' ON CONFLICT DO NOTHING'

        # 4. Translate date functions
        query = query.replace("strftime('%m', transaction_date)", "substr(transaction_date, 6, 2)")
        query = query.replace("strftime('%Y', transaction_date)", "substr(transaction_date, 1, 4)")
        query = query.replace("date('now','-7 days')", "CURRENT_DATE - INTERVAL '7 days'")
        query = query.replace("date(transaction_date)", "transaction_date::date")

        if params is not None:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def executemany(self, query, params_list):
        query = query.replace('?', '%s')
        query = query.replace('INSERT OR IGNORE', 'INSERT')
        if 'INSERT INTO categories' in query:
            query = query + ' ON CONFLICT DO NOTHING'
        self.cursor.executemany(query, params_list)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()

    @property
    def description(self):
        return self.cursor.description

class PostgresConnectionWrapper:
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return PostgresCursorWrapper(self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

def get_db_connection():
    db_url = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL")
    if db_url:
        import psycopg2
        # Clean URL format for PostgreSQL connection compatibility
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        conn = psycopg2.connect(db_url)
        return PostgresConnectionWrapper(conn)
    else:
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