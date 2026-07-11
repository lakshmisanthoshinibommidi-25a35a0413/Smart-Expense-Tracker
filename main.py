#! /usr/bin/env python3
from database import create_tables
from auth import register_user, login_user
from transaction import add_income, add_expense
from menu import display_menu
from reports import (
    view_transactions,
    search_transactions,
    financial_summary
)
from report_generator import generate_reports
from charts import view_charts
from category_manager import manage_categories
from dashboard import show_dashboard
from budget import budget_menu

def main():
    create_tables()  # Ensure the database and tables are created before starting the application
    logged_in_user = None

    while True:
        display_menu(logged_in_user)

        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()

        elif choice == "2":
            logged_in_user = login_user()

            if logged_in_user:
                show_dashboard(logged_in_user)

        elif choice == "3":
            if logged_in_user:
                add_income(logged_in_user)
            else:
                print("Please login first.")

        elif choice == "4":
            if logged_in_user:
                add_expense(logged_in_user)
            else:
                print("Please login first.")

        elif choice == "5":
            if logged_in_user:
                view_transactions(logged_in_user)
            else:
                print("Please login first.")

        elif choice == "6":
            if logged_in_user:
                search_transactions(logged_in_user)
            else:
                print("Please login first.")

        elif choice == "7":
            if logged_in_user:
                financial_summary(logged_in_user)
            else:
                print("Please login first.")

        elif choice == "8":
            if logged_in_user:
                generate_reports(logged_in_user)
            else:
                print("Please login first.")

        elif choice == "9":
            if logged_in_user:
                view_charts(logged_in_user)
            else:
                print("Please login first.")

        elif choice == "10":
            if logged_in_user:
                manage_categories()
            else:
                print("Please login first.")

        elif choice == "11":
            if logged_in_user:
                budget_menu(logged_in_user)
            else:
                print("Please login first.")

        elif choice == "12":
            if logged_in_user:
                logged_in_user = None
                print("Logged out successfully.")
            else:
                print("You are not logged in.")

        elif choice == "0":
            print("Thank you for using Smart Expense Tracker!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()



