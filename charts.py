import matplotlib.pyplot as plt

from repository import (
    get_category_summary,
    get_monthly_transactions
)

from utils import (
    print_header
)

def view_charts(user):

    while True:

        print_header("VIEW CHARTS")

        print("1. Expense Distribution (Pie Chart)")
        print("2. Monthly Expense Comparison (Bar Chart)")
        print("3. Back")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            expense_pie_chart(user)

        elif choice == "2":
            monthly_bar_chart(user)

        elif choice == "3":
            break

        else:
            print("\nInvalid Choice.")

def expense_pie_chart(user):

    summary = get_category_summary(user["id"])

    if not summary:
        print("\nNo expense data available.")
        return

    labels = []
    amounts = []

    for category, amount in summary:
        labels.append(category)
        amounts.append(amount)

    plt.figure(figsize=(8, 8))

    plt.pie(
        amounts,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Expense Distribution by Category")

    plt.axis("equal")

    plt.show()

def monthly_bar_chart(user):
    """
    Display Monthly Expense Comparison using Bar Chart.
    """

    year = input("\nEnter Year (YYYY): ").strip()

    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    monthly_expenses = []

    for month in range(1, 13):

        transactions = get_monthly_transactions(
            user["id"],
            month,
            year
        )

        total = 0

        for transaction in transactions:

            # Expense transactions only
            if transaction[1] == "Expense":
                total += transaction[3]

        monthly_expenses.append(total)

    plt.figure(figsize=(11, 5))

    plt.bar(
        months,
        monthly_expenses
    )

    plt.title(f"Monthly Expense Comparison ({year})")
    plt.xlabel("Month")
    plt.ylabel("Expense Amount")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.show()