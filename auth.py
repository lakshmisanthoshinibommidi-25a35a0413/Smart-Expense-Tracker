import hashlib
import sqlite3
from datetime import datetime
from database import get_db_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():

    print("\n========== USER REGISTRATION ==========")

    username = input("Enter Username : ").strip()

    password = input("Enter Password : ")

    confirm_password = input("Confirm Password : ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    hashed_password = hash_password(password)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users
            (username,password,created_at)
            VALUES(?,?,?)
        """,
        (
            username,
            hashed_password,
            created_at
        ))

        connection.commit()

        print("Registration Successful.")

    except sqlite3.IntegrityError:

        print("Username already exists.")

    finally:

        connection.close()


def login_user():

    print("\n========== USER LOGIN ==========")

    username = input("Username : ").strip()

    password = input("Password : ")

    hashed_password = hash_password(password)

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
    """, (username, hashed_password))

    user = cursor.fetchone()

    connection.close()

    if user:

        print(f"\nWelcome {user[1]}")

        return {
            "id": user[0],
            "username": user[1]
        }

    print("Invalid Username or Password")

    return None