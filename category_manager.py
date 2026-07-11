from constants import (
    INCOME_CATEGORIES,
    EXPENSE_CATEGORIES
)

from repository import (
    get_categories,
    add_category as repo_add_category,
    update_category,
    delete_category as repo_delete_category
)

def manage_categories():

    while True:

        print("\n" + "=" * 45)
        print("MANAGE CATEGORIES")
        print("=" * 45)

        print("1. View Categories")
        print("2. Add Category")
        print("3. Modify Category")
        print("4. Delete Category")
        print("5. Back")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            view_categories()

        elif choice == "2":
            add_category()

        elif choice == "3":
            modify_category()

        elif choice == "4":
            delete_category()

        elif choice == "5":
            break

        else:
            print("Invalid Choice.")

def view_categories():

    print("\nINCOME CATEGORIES")
    print("-" * 35)

    income_categories = get_categories("Income")

    for index, (_, category_name) in enumerate(income_categories, start=1):
        print(f"{index:<3}. {category_name}")

    print("\nEXPENSE CATEGORIES")
    print("-" * 35)

    expense_categories = get_categories("Expense")

    for index, (_, category_name) in enumerate(expense_categories, start=1):
        print(f"{index:<3}. {category_name}")

def add_category():

    print("\n1. Income")
    print("2. Expense")

    choice = input("Category Type: ").strip()

    if choice == "1":
        category_type = "Income"
    elif choice == "2":
        category_type = "Expense"
    else:
        print("Invalid choice.")
        return

    category_name = input("Enter New Category: ").strip()

    if not category_name:
        print("Category cannot be empty.")
        return

    repo_add_category(category_type, category_name)

    print("Category added successfully.")

def modify_category():

    print("\n1. Income")
    print("2. Expense")

    choice = input("\nSelect Category Type: ").strip()

    if choice == "1":
        category_type = "Income"
    elif choice == "2":
        category_type = "Expense"
    else:
        print("Invalid choice.")
        return

    categories = get_categories(category_type)

    if not categories:
        print("No categories found.")
        return

    print(f"\n{category_type.upper()} CATEGORIES")
    print("-" * 35)

    for index, (_, name) in enumerate(categories, start=1):
        print(f"{index}. {name}")

    selection = input("\nEnter category number: ").strip()

    if not selection.isdigit():
        print("Invalid selection.")
        return

    selection = int(selection)

    if selection < 1 or selection > len(categories):
        print("Invalid selection.")
        return

    category_id = categories[selection - 1][0]

    new_name = input("Enter new category name: ").strip()

    if not new_name:
        print("Category name cannot be empty.")
        return

    update_category(category_id, new_name)

    print("\nCategory updated successfully.")

def delete_category():

    print("\n1. Income")
    print("2. Expense")

    choice = input("\nSelect Category Type: ").strip()

    if choice == "1":
        category_type = "Income"
    elif choice == "2":
        category_type = "Expense"
    else:
        print("Invalid choice.")
        return

    categories = get_categories(category_type)

    if not categories:
        print("No categories found.")
        return

    print(f"\n{category_type.upper()} CATEGORIES")
    print("-" * 35)

    for index, (_, name) in enumerate(categories, start=1):
        print(f"{index}. {name}")

    selection = input("\nEnter category number: ").strip()

    if not selection.isdigit():
        print("Invalid selection.")
        return

    selection = int(selection)

    if selection < 1 or selection > len(categories):
        print("Invalid selection.")
        return

    category_id = categories[selection - 1][0]

    repo_delete_category(category_id)

    print("\nCategory deleted successfully.")