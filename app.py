import os
import csv
import io
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, Response
from database import create_tables, get_db_connection
import repository
from auth import hash_password

app = Flask(__name__)

# Ensure DB tables are created
create_tables()

# Utility to check X-User-Id header or query parameters
def get_user_id():
    user_id = request.headers.get('X-User-Id')
    if not user_id:
        user_id = request.args.get('user_id')
    if not user_id:
        return None
    try:
        return int(user_id)
    except ValueError:
        return None

# Root Welcome Endpoint
@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Smart Expense Tracker REST API",
        "version": "1.0.0"
    })

# User Registration Endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    if password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match."}), 400

    hashed = hash_password(password)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)", 
                       (username, hashed, created_at))
        connection.commit()
        return jsonify({"success": True, "message": "Registration successful! Welcome."})
    except Exception as e:
        # Username unique violation
        return jsonify({"success": False, "message": "Username already exists."}), 400
    finally:
        connection.close()

# User Login Endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    hashed = hash_password(password)
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, hashed))
    user = cursor.fetchone()
    connection.close()

    if user:
        return jsonify({
            "success": True,
            "user": {
                "id": user[0],
                "username": user[1]
            }
        })
    return jsonify({"success": False, "message": "Invalid username or password."}), 401

# Dashboard Statistics API
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    today = datetime.today()
    month = today.month
    year = today.year

    # 1. Financial Summary
    total_income, total_expense = repository.get_financial_summary(user_id)
    balance = total_income - total_expense

    # 2. Highest expense category
    highest_result = repository.get_highest_expense_category(user_id)
    highest_category = {"category": highest_result[0], "amount": highest_result[1]} if highest_result else None

    # 3. Most frequent expense category
    freq_result = repository.get_most_frequent_category(user_id)
    most_frequent = {"category": freq_result[0], "count": freq_result[1]} if freq_result else None

    # 4. Budget Status
    budget = repository.get_budget(user_id, month, year)
    spent_this_month = repository.get_monthly_expense_total(user_id, month, year)
    budget_remaining = (budget - spent_this_month) if budget is not None else 0
    budget_usage = (spent_this_month / budget * 100) if budget else 0

    # 5. Recent 5 Transactions
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, transaction_type, category, amount, description, transaction_date
        FROM transactions
        WHERE user_id = ?
        ORDER BY transaction_date DESC, id DESC
        LIMIT 5
    """, (user_id,))
    recent_raw = cursor.fetchall()
    connection.close()

    recent_transactions = []
    for row in recent_raw:
        recent_transactions.append({
            "id": row[0],
            "transaction_type": row[1],
            "category": row[2],
            "amount": row[3],
            "description": row[4],
            "transaction_date": row[5]
        })

    # 6. Chart Category-wise Summary (Pie Chart data)
    summary_raw = repository.get_category_summary(user_id)
    category_labels = [r[0] for r in summary_raw]
    category_values = [r[1] for r in summary_raw]

    # 7. Chart Monthly summary of the current year (Bar Chart data)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_expenses = []
    for m in range(1, 13):
        m_transactions = repository.get_monthly_transactions(user_id, m, year)
        m_total = sum(t[3] for t in m_transactions if t[1] == 'Expense')
        monthly_expenses.append(m_total)

    return jsonify({
        "success": True,
        "summary": {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "highest_expense_category": highest_category,
            "most_frequent_category": most_frequent
        },
        "budget": {
            "monthly_budget": budget,
            "spent": spent_this_month,
            "remaining": budget_remaining,
            "usage_percentage": budget_usage
        },
        "recent_transactions": recent_transactions,
        "chart_data": {
            "categories": {
                "labels": category_labels,
                "values": category_values
            },
            "monthly": {
                "labels": months,
                "values": monthly_expenses,
                "year": year
            }
        }
    })

# Transactions Endpoints (GET, POST, DELETE)
@app.route('/api/transactions', methods=['GET', 'POST'])
def manage_transactions():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    if request.method == 'GET':
        # Supported query parameters for advanced filtering/searching
        t_type = request.args.get('type') # 'Income' or 'Expense'
        category = request.args.get('category')
        min_amount = request.args.get('min_amount')
        max_amount = request.args.get('max_amount')
        date_val = request.args.get('date')
        search_query = request.args.get('search')

        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = """
            SELECT id, transaction_type, category, amount, description, transaction_date
            FROM transactions
            WHERE user_id = ?
        """
        params = [user_id]

        if t_type:
            query += " AND transaction_type = ?"
            params.append(t_type)
        if category:
            query += " AND category = ?"
            params.append(category)
        if min_amount:
            try:
                query += " AND amount >= ?"
                params.append(float(min_amount))
            except ValueError:
                pass
        if max_amount:
            try:
                query += " AND amount <= ?"
                params.append(float(max_amount))
            except ValueError:
                pass
        if date_val:
            query += " AND transaction_date = ?"
            params.append(date_val)
        if search_query:
            query += " AND (description LIKE ? OR category LIKE ?)"
            params.append(f"%{search_query}%")
            params.append(f"%{search_query}%")

        query += " ORDER BY transaction_date DESC, id DESC"
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        connection.close()

        transactions = []
        for r in rows:
            transactions.append({
                "id": r[0],
                "transaction_type": r[1],
                "category": r[2],
                "amount": r[3],
                "description": r[4],
                "transaction_date": r[5]
            })
        return jsonify({"success": True, "transactions": transactions})

    elif request.method == 'POST':
        data = request.get_json() or {}
        transaction_type = data.get('transaction_type') # 'Income' or 'Expense'
        category = data.get('category')
        amount = data.get('amount')
        description = data.get('description', '')
        transaction_date = data.get('transaction_date')

        if not transaction_type or not category or amount is None or not transaction_date:
            return jsonify({"success": False, "message": "Missing required fields."}), 400

        try:
            amount_val = float(amount)
            if amount_val <= 0:
                return jsonify({"success": False, "message": "Amount must be greater than zero."}), 400
        except ValueError:
            return jsonify({"success": False, "message": "Invalid amount number."}), 400

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            repository.insert_transaction(
                user_id=user_id,
                transaction_type=transaction_type,
                category=category,
                amount=amount_val,
                description=description,
                transaction_date=transaction_date,
                created_at=created_at
            )
            
            # Check budget alerts if it is an expense
            budget_alert = None
            if transaction_type == 'Expense':
                # Parse month/year from transaction_date
                try:
                    dt = datetime.strptime(transaction_date, "%Y-%m-%d")
                    m, y = dt.month, dt.year
                    budget = repository.get_budget(user_id, m, y)
                    if budget:
                        spent = repository.get_monthly_expense_total(user_id, m, y)
                        if spent > budget:
                            budget_alert = f"Alert! You have exceeded your monthly budget by ${spent - budget:.2f}."
                        elif spent >= budget * 0.9:
                            budget_alert = f"Warning! You have used {spent/budget*100:.1f}% of your monthly budget."
                except Exception:
                    pass

            return jsonify({
                "success": True, 
                "message": "Transaction added successfully!",
                "budget_alert": budget_alert
            })
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/transactions/<int:t_id>', methods=['DELETE'])
def delete_transaction(t_id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    try:
        repository.delete_transaction(t_id, user_id)
        return jsonify({"success": True, "message": "Transaction deleted successfully."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Categories Endpoints (GET, POST, PUT, DELETE)
@app.route('/api/categories', methods=['GET', 'POST'])
def manage_categories():
    user_id = get_user_id()
    if not user_id:
        # For default categories, we can allow fetching without login, but write operations require authentication.
        pass

    if request.method == 'GET':
        c_type = request.args.get('type') # 'Income' or 'Expense'
        connection = get_db_connection()
        cursor = connection.cursor()
        if c_type:
            cursor.execute("SELECT id, category_type, category_name FROM categories WHERE category_type = ? ORDER BY category_name", (c_type,))
        else:
            cursor.execute("SELECT id, category_type, category_name FROM categories ORDER BY category_type, category_name")
        rows = cursor.fetchall()
        connection.close()

        categories = []
        for r in rows:
            categories.append({
                "id": r[0],
                "category_type": r[1],
                "category_name": r[2]
            })
        return jsonify({"success": True, "categories": categories})

    elif request.method == 'POST':
        # Add new category (Admin or User level)
        data = request.get_json() or {}
        category_type = data.get('category_type') # 'Income' or 'Expense'
        category_name = data.get('category_name', '').strip()

        if not category_type or not category_name:
            return jsonify({"success": False, "message": "Missing type or name."}), 400

        try:
            repository.add_category(category_type, category_name)
            return jsonify({"success": True, "message": "Category added successfully."})
        except Exception:
            return jsonify({"success": False, "message": "Category already exists."}), 400

@app.route('/api/categories/<int:c_id>', methods=['PUT', 'DELETE'])
def manage_category_item(c_id):
    # Edit or delete category
    if request.method == 'PUT':
        data = request.get_json() or {}
        new_name = data.get('category_name', '').strip()
        if not new_name:
            return jsonify({"success": False, "message": "New name cannot be empty."}), 400
        try:
            repository.update_category(c_id, new_name)
            return jsonify({"success": True, "message": "Category updated successfully."})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
    elif request.method == 'DELETE':
        try:
            repository.delete_category(c_id)
            return jsonify({"success": True, "message": "Category deleted successfully."})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

# Budget Endpoints (GET, POST)
@app.route('/api/budget', methods=['GET', 'POST'])
def manage_budget():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    if request.method == 'GET':
        month = request.args.get('month', datetime.today().month)
        year = request.args.get('year', datetime.today().year)
        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return jsonify({"success": False, "message": "Invalid parameters."}), 400

        budget = repository.get_budget(user_id, month, year)
        spent = repository.get_monthly_expense_total(user_id, month, year)

        return jsonify({
            "success": True,
            "month": month,
            "year": year,
            "monthly_budget": budget,
            "spent": spent,
            "remaining": (budget - spent) if budget is not None else 0
        })

    elif request.method == 'POST':
        data = request.get_json() or {}
        amount = data.get('amount')
        month = data.get('month', datetime.today().month)
        year = data.get('year', datetime.today().year)

        if amount is None:
            return jsonify({"success": False, "message": "Amount is required."}), 400

        try:
            amount_val = float(amount)
            if amount_val <= 0:
                return jsonify({"success": False, "message": "Budget must be greater than zero."}), 400
            month = int(month)
            year = int(year)
        except ValueError:
            return jsonify({"success": False, "message": "Invalid numeric values."}), 400

        existing = repository.get_budget(user_id, month, year)
        if existing is not None:
            repository.update_budget(user_id, amount_val, month, year)
        else:
            repository.save_budget(user_id, amount_val, month, year)

        return jsonify({"success": True, "message": "Budget saved successfully."})

# Export CSV Report Endpoint
@app.route('/api/reports/export', methods=['GET'])
def export_report():
    user_id = get_user_id()
    if not user_id:
        return "Unauthorized", 401

    report_type = request.args.get('report_type', 'monthly') # 'monthly', 'annual', 'category'
    year = request.args.get('year', datetime.today().year)
    month = request.args.get('month', datetime.today().month)

    try:
        year = int(year)
        month = int(month)
    except ValueError:
        return "Invalid parameters", 400

    output = io.StringIO()
    writer = csv.writer(output)

    if report_type == 'monthly':
        months_list = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month_name = months_list[month - 1] if 1 <= month <= 12 else str(month)
        filename = f"Monthly_Report_{month_name}_{year}.csv"

        transactions = repository.get_monthly_transactions(user_id, month, year)
        writer.writerow(["ID", "Type", "Category", "Amount", "Description", "Date"])
        for t in transactions:
            writer.writerow(t)

    elif report_type == 'annual':
        filename = f"Annual_Report_{year}.csv"
        transactions = repository.get_yearly_transactions(user_id, year)
        writer.writerow(["ID", "Type", "Category", "Amount", "Description", "Date"])
        for t in transactions:
            writer.writerow(t)

    elif report_type == 'category':
        filename = "Category_Report.csv"
        summary = repository.get_category_summary(user_id)
        writer.writerow(["Category", "Total Expense"])
        for s in summary:
            writer.writerow(s)
    else:
        return "Invalid report type", 400

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

if __name__ == '__main__':
    # Start local development web server
    print("Starting Smart Expense Tracker Web Application on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
