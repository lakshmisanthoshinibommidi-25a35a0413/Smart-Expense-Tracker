from datetime import datetime

from repository import (
    insert_transaction,
    get_categories
)

from database import get_db_connection

from constants import (
    INCOME,
    EXPENSE
)


def choose_category(transaction_type):
    categories = get_categories(transaction_type)

    if not categories:
        print("\nNo categories available.")
        return None

    print(f"\n{transaction_type.upper()} CATEGORIES")
    print("-" * 40)

    for index, (_, category_name) in enumerate(categories, start=1):
        print(f"{index}. {category_name}")

    while True:
        choice = input("\nSelect Category : ").strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(categories):
                return categories[choice - 1][1]

        print("Invalid choice. Please try again.")


def add_transaction(user, transaction_type):

    print(f"\n========== ADD {transaction_type.upper()} ==========")

    category = choose_category(transaction_type)

    description = input("Description : ").strip()

    while True:

        try:

            amount = float(input("Amount (₹): "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            break

        except ValueError:

            print("Please enter a valid amount.")

    transaction_date = input(
        "Enter Date (YYYY-MM-DD) or press Enter for today: "
    ).strip()

    if not transaction_date:
        transaction_date = datetime.today().strftime("%Y-%m-%d")

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_transaction(
        user["id"],
        transaction_type,
        category,
        amount,
        description,
        transaction_date,
        created_at
    )

    print(f"\n{transaction_type} added successfully.")


def add_income(user):
    add_transaction(user, INCOME)


def add_expense(user):
    add_transaction(user, EXPENSE)