# 💰 Smart Expense Tracker

A console-based Personal Expense Tracker developed using **Python** and **SQLite**. This application helps users manage their income, expenses, budgets, reports, and financial insights through a simple menu-driven interface.

---

## 📌 Features

### 👤 User Management

* User Registration
* Secure Login (Password Hashing)

### 💵 Transaction Management

* Add Income
* Add Expense
* View All Transactions
* Search Transactions

  * By Category
  * By Transaction Type
  * By Date
  * By Amount Range

### 📂 Category Management

* View Categories
* Add New Category
* Modify Existing Category
* Delete Category

### 📊 Expense Tracking

* Monthly Expenses
* Weekly Expenses
* Category-wise Expenses

### 📈 Financial Summary

* Total Income
* Total Expense
* Current Balance
* Highest Expense Category
* Most Frequent Expense Category

### 📄 Reports

* Monthly Financial Report
* Annual Financial Report
* Category-wise Expense Report
* Export Reports to CSV

### 📉 Data Visualization

* Pie Chart (Category-wise Expenses)
* Bar Chart (Monthly Expenses)

### 🎯 Budget Management

* Set Monthly Budget
* View Budget
* Update Budget
* Budget Analysis
* Budget Usage Percentage

---

## 🛠 Technologies Used

* Python 3.13
* SQLite3
* Matplotlib
* CSV
* Hashlib
* Datetime

---

## 📁 Project Structure

```text
SmartExpenseTracker/
│
├── data/
│   └── expense.db
│
├── exports/
│
├── auth.py
├── budget.py
├── category_manager.py
├── charts.py
├── constants.py
├── dashboard.py
├── database.py
├── main.py
├── menu.py
├── report_generator.py
├── reports.py
├── repository.py
├── transaction.py
├── utils.py
└── README.md
```

---

## ▶️ How to Run

1. Clone the repository.
2. Create a virtual environment.

```bash
python3 -m venv .venv
```

3. Activate the virtual environment.

**macOS/Linux**

```bash
source .venv/bin/activate
```

**Windows**

```cmd
.venv\Scripts\activate
```

4. Install dependencies.

```bash
pip install matplotlib
```

5. Run the application.

```bash
python3 main.py
```

---

## 📷 Sample Features

* Register/Login
* Dashboard
* Transaction Management
* Reports
* Charts
* Budget Analysis
* CSV Export

---

## 👨‍💻 Author

Developed by **Santhur**

Python • SQLite • Matplotlib
