from constants import (
    INCOME,
    EXPENSE
)
from transaction import choose_category
from repository import (
    get_all_transactions,
    get_transactions_by_category,
    get_transactions_by_type,
    get_transactions_by_date,
    get_financial_summary,
    get_transactions_by_amount_range,
    get_monthly_expenses,
    get_weekly_expenses,
    get_category_expenses,
    get_highest_expense_category,
    get_most_frequent_category
)
from utils import format_currency
from utils import choose_month


def display_transactions(transactions):
    """
    Display transactions in tabular format.
    """

    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n" + "=" * 125)

    print(
        f"{'ID':<5} "
        f"{'TYPE':<12} "
        f"{'CATEGORY':<20} "
        f"{'AMOUNT':>15} "
        f"{'DATE':<12} "
        f"{'DESCRIPTION'}"
    )

    print("=" * 125)

    for transaction in transactions:

        print(
            f"{transaction[0]:<5} "
            f"{transaction[1]:<12} "
            f"{transaction[2]:<20} "
            f"{format_currency(transaction[3]):>15} "
            f"{transaction[5]:<12} "
            f"{transaction[4]}"
        )

    print("=" * 125)

def view_transactions(user):
    """
    View all transactions.
    """

    transactions = get_all_transactions(user["id"])

    display_transactions(transactions)

def search_by_category(user):
    """
    Search transactions by category.
    """

    print("\n========== SEARCH BY CATEGORY ==========")
    print("1. Income Categories")
    print("2. Expense Categories")

    choice = input("\nEnter Choice : ").strip()

    if choice == "1":
        category = choose_category(INCOME)

    elif choice == "2":
        category = choose_category(EXPENSE)

    else:
        print("Invalid Choice.")
        return

    transactions = get_transactions_by_category(
        user["id"],
        category
    )

    display_transactions(transactions)


def search_by_type(user):
    """
    Search by transaction type.
    """

    print("\n1. Income")
    print("2. Expense")

    choice = input("Choose : ")

    if choice == "1":
        transaction_type = INCOME

    elif choice == "2":
        transaction_type = EXPENSE

    else:
        print("Invalid Choice.")
        return

    transactions = get_transactions_by_type(
        user["id"],
        transaction_type
    )

    display_transactions(transactions)


def search_by_date(user):
    """
    Search by date.
    """

    transaction_date = input(
        "\nEnter Date (YYYY-MM-DD): "
    ).strip()

    transactions = get_transactions_by_date(
        user["id"],
        transaction_date
    )

    display_transactions(transactions)


def search_transactions(user):
    """
    Search Transactions Menu
    """

    while True:

        print("\n========== SEARCH TRANSACTIONS ==========")
        print("1. Search by Category")
        print("2. Search by Type")
        print("3. Search by Date")
        print("4. Search by Amount Range")
        print("5. Filter Transactions")
        print("6. Back")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            search_by_category(user)

        elif choice == "2":
            search_by_type(user)

        elif choice == "3":
            search_by_date(user)

        elif choice == "4":
            search_by_amount(user)

        elif choice == "5":
            filter_transactions(user)

        elif choice == "6":
            break

        else:
            print("\n❌ Invalid Choice. Please try again.")

def filter_transactions(user):

    while True:

        print("\n========== FILTER TRANSACTIONS ==========")
        print("1. Monthly Expenses")
        print("2. Weekly Expenses")
        print("3. Category-wise Expenses")
        print("4. Back")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            filter_monthly_expenses(user)

        elif choice == "2":
            filter_weekly_expenses(user)

        elif choice == "3":
            filter_category_expenses(user)

        elif choice == "4":
            break

        else:
            print("Invalid Choice.")

def filter_monthly_expenses(user):

    month_number, month_name = choose_month()

    year = input("\nEnter Year (YYYY): ").strip()

    transactions = get_monthly_expenses(
        user["id"],
        month_number,
        year
    )

    print("\n" + "=" * 60)
    print(f"MONTHLY EXPENSES - {month_name} {year}".center(60))
    print("=" * 60)

    display_transactions(transactions)

def filter_weekly_expenses(user):
    """
    Display expenses for the last 7 days.
    """

    transactions = get_weekly_expenses(user["id"])

    print("\n" + "=" * 60)
    print("WEEKLY EXPENSES (LAST 7 DAYS)".center(60))
    print("=" * 60)

    display_transactions(transactions)

def filter_category_expenses(user):
    """
    Display expenses for a selected category.
    """

    print("\n========== CATEGORY-WISE EXPENSES ==========")

    category = choose_category(EXPENSE)

    transactions = get_category_expenses(
        user["id"],
        category
    )

    print("\n" + "=" * 60)
    print(f"EXPENSE CATEGORY - {category}".center(60))
    print("=" * 60)

    display_transactions(transactions)

def financial_summary(user):
    """
    Display financial summary.
    """

    total_income, total_expense = get_financial_summary(user["id"])

    balance = total_income - total_expense

    highest_category = get_highest_expense_category(user["id"])
    frequent_category = get_most_frequent_category(user["id"])

    print("\n" + "=" * 60)
    print("FINANCIAL SUMMARY".center(60))
    print("=" * 60)

    print(f"{'Total Income':<30}: {format_currency(total_income)}")
    print(f"{'Total Expense':<30}: {format_currency(total_expense)}")
    print(f"{'Current Balance':<30}: {format_currency(balance)}")

    print("-" * 60)

    if highest_category:
        print(
            f"{'Highest Expense Category':<30}: "
            f"{highest_category[0]} ({format_currency(highest_category[1])})"
        )
    else:
        print(f"{'Highest Expense Category':<30}: N/A")

    if frequent_category:
        print(
            f"{'Most Frequent Category':<30}: "
            f"{frequent_category[0]} ({frequent_category[1]} transactions)"
        )
    else:
        print(f"{'Most Frequent Category':<30}: N/A")

    print("=" * 60)


def search_by_amount(user):

    print("\n========== SEARCH BY AMOUNT ==========")

    try:

        minimum = float(input("Enter Minimum Amount : "))
        maximum = float(input("Enter Maximum Amount : "))

    except ValueError:

        print("Invalid amount entered.")
        return

    if minimum > maximum:

        print("Minimum amount cannot be greater than Maximum amount.")
        return

    transactions = get_transactions_by_amount_range(
        user["id"],
        minimum,
        maximum
    )

    display_transactions(transactions)