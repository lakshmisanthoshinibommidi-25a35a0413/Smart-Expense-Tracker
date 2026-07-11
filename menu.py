#! /bin env python3

import os
import datetime


print("its a smart expense tracker system")
print ("--------------------------------")
print("Welcome to the Smart Expense Tracker System!")
print("This system helps you track your expenses and manage your budget effectively.")
print("Let's get started by entering your expenses.")
print("please choose below categories to make an entries")

def display_menu(logged_in_user=None):

    print("\n" + "=" * 55)
    print("SMART EXPENSE TRACKER SYSTEM".center(55))
    print("=" * 55)

    if logged_in_user:
        print(f"Logged in as : {logged_in_user['username']}")
        print("-" * 55)

    print("1. Register")
    print("2. Login")
    print("-" * 55)
    print("3. Add Income")
    print("4. Add Expense")
    print("5. View Transactions")
    print("6. Search Transactions")
    print("7. Financial Summary")
    print("8. Generate Reports")
    print("9. View Charts")
    print("10. Manage Categories")
    print("11. Set Budget")
    print("12. Logout")
    print("0. Exit")
    print("=" * 55)