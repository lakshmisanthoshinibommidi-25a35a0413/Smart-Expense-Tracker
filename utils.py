def format_currency(amount):
    """Return amount formatted as Indian Rupees."""
    return f"₹{amount:,.2f}"

def print_header(title):

    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50)

def choose_month():
    """
    Display a list of months and return the selected month number and name.
    """

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    print("\nSelect Month")
    print("-" * 30)

    for index, month in enumerate(months, start=1):
        print(f"{index}. {month}")

    while True:
        try:
            choice = int(input("\nEnter Choice : "))

            if 1 <= choice <= 12:
                return choice, months[choice - 1]

            print("❌ Please enter a number between 1 and 12.")

        except ValueError:
            print("❌ Invalid input. Please enter a number.")
