from datetime import datetime

from repository import (
    get_budget,
    save_budget,
    update_budget,
    get_monthly_expense_total
)

from utils import (
    format_currency,
    print_header
)

def budget_menu(user):

    while True:

        print_header("BUDGET MANAGEMENT")

        print("1. Set Monthly Budget")
        print("2. View Current Budget")
        print("3. Update Budget")
        print("4. Budget Analysis")
        print("5. Back")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            set_budget(user)

        elif choice == "2":
            view_budget(user)

        elif choice == "3":
            modify_budget(user)

        elif choice == "4":
            budget_analysis(user)

        elif choice == "5":
            break

        else:
            print("Invalid Choice.")

def set_budget(user):

    today = datetime.today()

    month = today.month
    year = today.year

    existing_budget = get_budget(
        user["id"],
        month,
        year
    )

    if existing_budget:

        print("\nBudget already exists for this month.")
        print(f"Current Budget : {format_currency(existing_budget)}")
        return

    try:

        amount = float(
            input("\nEnter Monthly Budget : ")
        )

        if amount <= 0:
            print("Budget must be greater than zero.")
            return

    except ValueError:

        print("Invalid amount.")
        return

    save_budget(
        user["id"],
        amount,
        month,
        year
    )

    print("\n✅ Budget saved successfully.")

def view_budget(user):

    today = datetime.today()

    month = today.month
    year = today.year

    budget = get_budget(
        user["id"],
        month,
        year
    )

    print_header("CURRENT MONTH BUDGET")

    if budget is None:

        print("No budget has been set.")
        return

    print(f"Budget : {format_currency(budget)}")

def modify_budget(user):

    today = datetime.today()

    month = today.month
    year = today.year

    budget = get_budget(
        user["id"],
        month,
        year
    )

    if budget is None:

        print("No budget found.")
        return

    print(f"\nCurrent Budget : {format_currency(budget)}")

    try:

        new_budget = float(
            input("Enter New Budget : ")
        )

        if new_budget <= 0:
            print("Budget must be greater than zero.")
            return

    except ValueError:

        print("Invalid amount.")
        return

    update_budget(
        user["id"],
        new_budget,
        month,
        year
    )

    print("\n✅ Budget updated successfully.")

def budget_analysis(user):

    today = datetime.today()

    month = today.month
    year = today.year

    budget = get_budget(
        user["id"],
        month,
        year
    )

    if budget is None:

        print("\nNo budget found.")
        return

    spent = get_monthly_expense_total(
        user["id"],
        month,
        year
    )

    remaining = budget - spent

    usage = (spent / budget) * 100 if budget else 0

    print_header("BUDGET ANALYSIS")

    print(f"Budget        : {format_currency(budget)}")
    print(f"Spent         : {format_currency(spent)}")
    print(f"Remaining     : {format_currency(remaining)}")
    print(f"Usage         : {usage:.2f}%")

    print("-" * 45)

    if spent > budget:
        print(f"⚠ Budget exceeded by {format_currency(spent - budget)}")
    else:
        print("✅ You are within your budget.")
