from datetime import datetime

from repository import (
    get_financial_summary,
    get_highest_expense_category,
    get_most_frequent_category,
    get_transaction_count
)

from utils import (
    format_currency,
    print_header
)

def show_dashboard(user):

    print_header("SMART EXPENSE TRACKER DASHBOARD")

    total_income, total_expense = get_financial_summary(user["id"])

    balance = total_income - total_expense

    highest = get_highest_expense_category(user["id"])
    frequent = get_most_frequent_category(user["id"])

    transaction_count = get_transaction_count(user["id"])

    print(f"Welcome : {user['username']}")
    print(f"Date    : {datetime.today().strftime('%d-%m-%Y')}")

    print("-" * 50)

    print(f"Current Balance         {format_currency(balance)}")
    print(f"Total Income            {format_currency(total_income)}")
    print(f"Total Expense           {format_currency(total_expense)}")

    print("-" * 50)

    print(
        f"Highest Expense         "
        f"{highest if highest else 'N/A'}"
    )

    print(
        f"Most Frequent Category  "
        f"{frequent if frequent else 'N/A'}"
    )

    print("-" * 50)

    print(f"Transactions            {transaction_count}")

    print("=" * 50)