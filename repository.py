from database import get_db_connection


# -----------------------------
# Transaction Repository
# -----------------------------

def insert_transaction(
    user_id,
    transaction_type,
    category,
    amount,
    description,
    transaction_date,
    created_at
):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (
            user_id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        user_id,
        transaction_type,
        category,
        amount,
        description,
        transaction_date,
        created_at
    ))

    connection.commit()
    connection.close()


def get_all_transactions(user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id=?
        ORDER BY transaction_date DESC,id DESC
    """, (user_id,))

    transactions = cursor.fetchall()

    connection.close()

    return transactions


def get_transactions_by_category(user_id, category):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id=?
        AND category LIKE ?
        ORDER BY transaction_date DESC,id DESC
    """,
    (
        user_id,
        f"%{category}%"
    ))

    transactions = cursor.fetchall()

    connection.close()

    return transactions


def get_transactions_by_type(user_id, transaction_type):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id=?
        AND transaction_type=?
        ORDER BY transaction_date DESC,id DESC
    """,
    (
        user_id,
        transaction_type
    ))

    transactions = cursor.fetchall()

    connection.close()

    return transactions


def get_transactions_by_date(user_id, transaction_date):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id=?
        AND transaction_date=?
        ORDER BY id DESC
    """,
    (
        user_id,
        transaction_date
    ))

    transactions = cursor.fetchall()

    connection.close()

    return transactions


def get_financial_summary(user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM transactions
        WHERE user_id=?
        AND transaction_type='Income'
    """, (user_id,))

    total_income = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM transactions
        WHERE user_id=?
        AND transaction_type='Expense'
    """, (user_id,))

    total_expense = cursor.fetchone()[0]

    connection.close()

    return total_income, total_expense

def get_monthly_transactions(user_id, month, year):

    connection = get_db_connection()
    cursor = connection.cursor()

    month = f"{int(month):02d}"

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id = ?
        AND strftime('%m', transaction_date) = ?
        AND strftime('%Y', transaction_date) = ?
        ORDER BY transaction_date DESC, id DESC
    """,
    (
        user_id,
        month,
        str(year)
    ))

    transactions = cursor.fetchall()

    connection.close()

    return transactions

def get_yearly_transactions(user_id, year):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id = ?
        AND strftime('%Y', transaction_date) = ?
        ORDER BY transaction_date DESC, id DESC
    """,
    (
        user_id,
        str(year)
    ))

    transactions = cursor.fetchall()

    connection.close()

    return transactions

def get_category_summary(user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM transactions
        WHERE user_id = ?
        AND transaction_type = 'Expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """,
    (user_id,))

    summary = cursor.fetchall()

    connection.close()

    return summary

def get_transactions_by_amount_range(user_id, min_amount, max_amount):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id = ?
        AND amount BETWEEN ? AND ?
        ORDER BY transaction_date DESC, id DESC
    """,
    (
        user_id,
        min_amount,
        max_amount
    ))

    transactions = cursor.fetchall()

    connection.close()

    return transactions

def get_monthly_expenses(user_id, month, year):

    connection = get_db_connection()
    cursor = connection.cursor()

    month = f"{int(month):02d}"

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id = ?
        AND transaction_type = 'Expense'
        AND strftime('%m', transaction_date) = ?
        AND strftime('%Y', transaction_date) = ?
        ORDER BY transaction_date DESC, id DESC
    """,
    (user_id, month, str(year)))

    transactions = cursor.fetchall()

    connection.close()

    return transactions

def get_weekly_expenses(user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id = ?
        AND transaction_type = 'Expense'
        AND date(transaction_date) >= date('now','-7 days')
        ORDER BY transaction_date DESC, id DESC
    """,
    (user_id,))

    transactions = cursor.fetchall()

    connection.close()

    return transactions

def get_category_expenses(user_id, category):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date
        FROM transactions
        WHERE user_id = ?
        AND transaction_type = 'Expense'
        AND category = ?
        ORDER BY transaction_date DESC, id DESC
    """,
    (user_id, category))

    transactions = cursor.fetchall()

    connection.close()

    return transactions

def get_highest_expense_category(user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount) AS total
        FROM transactions
        WHERE user_id = ?
        AND transaction_type = 'Expense'
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    return result

def get_most_frequent_category(user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            COUNT(*) AS total
        FROM transactions
        WHERE user_id = ?
        AND transaction_type = 'Expense'
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    return result

def get_categories(category_type):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, category_name
        FROM categories
        WHERE category_type = ?
        ORDER BY category_name
    """, (category_type,))

    categories = cursor.fetchall()

    connection.close()

    return categories


def add_category(category_type, category_name):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO categories
        (category_type, category_name)
        VALUES (?, ?)
    """, (category_type, category_name))

    connection.commit()
    connection.close()


def update_category(category_id, new_name):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE categories
        SET category_name = ?
        WHERE id = ?
    """, (new_name, category_id))

    connection.commit()
    connection.close()


def delete_category(category_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
    """, (category_id,))

    connection.commit()
    connection.close()

def get_transaction_count(user_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id = ?
    """, (user_id,))

    count = cursor.fetchone()[0]

    connection.close()

    return count

def get_budget(user_id, month, year):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT monthly_budget
        FROM budgets
        WHERE user_id = ?
        AND month = ?
        AND year = ?
    """, (user_id, month, year))

    budget = cursor.fetchone()

    connection.close()

    return budget[0] if budget else None

def save_budget(user_id, amount, month, year):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO budgets
        (
            user_id,
            monthly_budget,
            month,
            year
        )
        VALUES (?, ?, ?, ?)
    """,
    (
        user_id,
        amount,
        month,
        year
    ))

    connection.commit()
    connection.close()

def update_budget(user_id, amount, month, year):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE budgets
        SET monthly_budget = ?
        WHERE user_id = ?
        AND month = ?
        AND year = ?
    """,
    (
        amount,
        user_id,
        month,
        year
    ))

    connection.commit()
    connection.close()

def get_monthly_expense_total(user_id, month, year):

    connection = get_db_connection()
    cursor = connection.cursor()

    month = f"{int(month):02d}"

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE user_id = ?
        AND transaction_type = 'Expense'
        AND strftime('%m', transaction_date) = ?
        AND strftime('%Y', transaction_date) = ?
    """,
    (
        user_id,
        month,
        str(year)
    ))

    total = cursor.fetchone()[0]

    connection.close()

    return total