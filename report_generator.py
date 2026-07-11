from repository import (
    get_monthly_transactions,
    get_yearly_transactions,
    get_category_summary
)

from reports import display_transactions
from utils import (
    format_currency,
    print_header,
    choose_month
)
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXPORT_DIR = os.path.join(BASE_DIR, "exports")

os.makedirs(EXPORT_DIR, exist_ok=True)

def generate_reports(user):

    while True:

        print("\n========== GENERATE REPORTS ==========")
        print("1. Monthly Financial Report")
        print("2. Annual Summary Report")
        print("3. Category-wise Expense Report")
        print("4. Export Monthly Report (CSV)")
        print("5. Export Annual Report (CSV)")
        print("6. Export Category Report (CSV)")
        print("7. Back")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            monthly_report(user)

        elif choice == "2":
            annual_report(user)

        elif choice == "3":
            category_report(user)

        elif choice == "4":
            export_monthly_report(user)

        elif choice == "5":
            export_annual_report(user)

        elif choice == "6":
            export_category_report(user)

        elif choice == "7":
            break

    else:
        print("Invalid Choice.")



def annual_report(user):
    """
    Generate Annual Financial Report.
    """

    year = input("\nEnter Year (YYYY): ").strip()

    transactions = get_yearly_transactions(
        user["id"],
        year
    )

    print_header(f"ANNUAL REPORT - {year}")

    if not transactions:
        print("\nNo transactions found.")
        return

    total_income = 0
    total_expense = 0

    for transaction in transactions:

        if transaction[1] == "Income":
            total_income += transaction[3]
        else:
            total_expense += transaction[3]

    savings = total_income - total_expense

    print(f"Total Income   : {format_currency(total_income)}")
    print(f"Total Expense  : {format_currency(total_expense)}")
    print(f"Savings        : {format_currency(savings)}")

    print("\nTransaction Details")
    display_transactions(transactions)

def category_report(user):
    """
    Generate Category-wise Expense Report.
    """

    summary = get_category_summary(user["id"])

    print_header("CATEGORY-WISE EXPENSE REPORT")

    if not summary:
        print("\nNo expense records found.")
        return

    print(f"{'Category':<25}{'Total Expense'}")
    print("-" * 45)

    grand_total = 0

    for category, amount in summary:

        grand_total += amount

        print(
            f"{category:<25}"
            f"{format_currency(amount)}"
        )

    print("-" * 45)
    print(f"{'Grand Total':<25}{format_currency(grand_total)}")

def monthly_report(user):
    """
    Generate Monthly Financial Report.
    """

    month_number, month_name = choose_month()

    year = input("\nEnter Year (YYYY): ").strip()

    transactions = get_monthly_transactions(
        user["id"],
        month_number,
        year
    )

    print_header(f"MONTHLY REPORT - {month_name} {year}")

    if not transactions:
        print("\nNo transactions found.")
        return

    total_income = 0
    total_expense = 0

    for transaction in transactions:

        if transaction[1] == "Income":
            total_income += transaction[3]
        else:
            total_expense += transaction[3]

    savings = total_income - total_expense

    print(f"Total Income   : {format_currency(total_income)}")
    print(f"Total Expense  : {format_currency(total_expense)}")
    print(f"Savings        : {format_currency(savings)}")

    print("\nTransaction Details")
    display_transactions(transactions)

def export_to_csv(filename, transactions):
    """
    Export transactions to CSV.
    """

    file_path = os.path.join(EXPORT_DIR, filename)

    with open(
        file_path,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Type",
            "Category",
            "Amount",
            "Description",
            "Date"
        ])

        for transaction in transactions:

            writer.writerow(transaction)

    print(f"\n✅ Report exported successfully.")
    print(f"Location : {file_path}")

def export_monthly_report(user):

    month_number, month_name = choose_month()

    year = input("\nEnter Year (YYYY): ").strip()

    transactions = get_monthly_transactions(
        user["id"],
        month_number,
        year
    )

    if not transactions:
        print("\nNo transactions found.")
        return

    filename = f"Monthly_Report_{month_name}_{year}.csv"

    export_to_csv(
        filename,
        transactions
    )

def export_annual_report(user):
    """
    Export Annual Report to CSV.
    """

    year = input("\nEnter Year (YYYY): ").strip()

    transactions = get_yearly_transactions(
        user["id"],
        year
    )

    if not transactions:
        print("\nNo transactions found.")
        return

    filename = f"Annual_Report_{year}.csv"

    export_to_csv(
        filename,
        transactions
    )

def export_category_report(user):
    """
    Export Category-wise Expense Report to CSV.
    """

    summary = get_category_summary(user["id"])

    if not summary:
        print("\nNo expense records found.")
        return

    filename = os.path.join(
        EXPORT_DIR,
        "Category_Report.csv"
    )

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Category",
            "Total Expense"
        ])

        for category, amount in summary:

            writer.writerow([
                category,
                amount
            ])

    print("\n✅ Category report exported successfully.")
    print(f"Location : {filename}")