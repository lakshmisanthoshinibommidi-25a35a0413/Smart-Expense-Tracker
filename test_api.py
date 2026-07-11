import urllib.request
import json
import sys
import time

BASE_URL = "http://127.0.0.1:5000"

def request_json(path, data=None, method="GET", headers=None):
    url = f"{BASE_URL}{path}"
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)
    
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            return json.loads(res_data)
    except urllib.error.HTTPError as e:
        error_data = e.read().decode("utf-8")
        try:
            return json.loads(error_data)
        except Exception:
            return {"success": False, "message": f"HTTP Error {e.code}: {e.reason}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def main():
    print("==================================================")
    print("   smart expense tracker - API Integration Test   ")
    print("==================================================")
    print()

    # Generate a unique username and category name for this test run
    unique_id = int(time.time())
    username = f"api_user_{unique_id}"
    category_name = f"Food_{unique_id}"

    # 1. Register user
    print(f"1. Testing Registration for {username}...")
    reg_payload = {
        "username": username,
        "password": "Password123",
        "confirm_password": "Password123"
    }
    res = request_json("/api/register", reg_payload, "POST")
    print("   Registration Result:", res)
    if not res.get("success"):
        print("   FAILED: Registration failed unexpectedly.")
        sys.exit(1)

    # 2. Login user
    print("\n2. Testing Login...")
    login_payload = {
        "username": username,
        "password": "Password123"
    }
    res = request_json("/api/login", login_payload, "POST")
    print("   Login Result:", res)
    if not res.get("success"):
        print("   FAILED: Login failed.")
        sys.exit(1)

    user_id = res["user"]["id"]
    auth_header = {"X-User-Id": str(user_id)}

    # 3. Add Custom Category
    print(f"\n3. Testing Add Custom Category ({category_name})...")
    cat_payload = {
        "category_type": "Expense",
        "category_name": category_name
    }
    res = request_json("/api/categories", cat_payload, "POST", auth_header)
    print("   Add Category Result:", res)

    # 4. Fetch Categories
    print("\n4. Testing Fetch Categories...")
    res = request_json("/api/categories", headers=auth_header)
    categories = res.get("categories", [])
    found = any(c["category_name"] == category_name for c in categories)
    print(f"   Found '{category_name}': {found} (Total: {len(categories)})")
    if not found:
        print("   FAILED: Added category not retrieved.")
        sys.exit(1)

    # 5. Set Budget Limit
    print("\n5. Testing Set Budget...")
    budget_payload = {
        "amount": 500.0,
        "month": 7,
        "year": 2026
    }
    res = request_json("/api/budget", budget_payload, "POST", auth_header)
    print("   Set Budget Result:", res)
    if not res.get("success"):
        print("   FAILED: Set budget failed.")
        sys.exit(1)

    # 6. Retrieve Budget
    print("\n6. Testing Retrieve Budget...")
    res = request_json("/api/budget?month=7&year=2026", headers=auth_header)
    print("   Retrieve Budget Result:", res)
    if res.get("monthly_budget") != 500.0:
        print(f"   FAILED: Budget value mismatch, expected 500.0 but got {res.get('monthly_budget')}")
        sys.exit(1)

    # 7. Add Transaction (Income)
    print("\n7. Testing Add Income Transaction...")
    inc_payload = {
        "transaction_type": "Income",
        "category": "Salary",
        "amount": 2000.0,
        "transaction_date": "2026-07-10",
        "description": "API Test Salary"
    }
    res = request_json("/api/transactions", inc_payload, "POST", auth_header)
    print("   Add Income Result:", res)
    if not res.get("success"):
        print("   FAILED: Add Income failed.")
        sys.exit(1)

    # 8. Add Transaction (Expense)
    print("\n8. Testing Add Expense Transaction...")
    exp_payload = {
        "transaction_type": "Expense",
        "category": category_name,
        "amount": 80.0,
        "transaction_date": "2026-07-11",
        "description": "API Test Lunch"
    }
    res = request_json("/api/transactions", exp_payload, "POST", auth_header)
    print("   Add Expense Result:", res)
    if not res.get("success"):
        print("   FAILED: Add Expense failed.")
        sys.exit(1)

    # 9. Verify Dashboard Summary
    print("\n9. Verify Dashboard Summary...")
    res = request_json("/api/dashboard", headers=auth_header)
    print("   Dashboard Stats:", res.get("summary"))
    print("   Dashboard Budget Usage:", res.get("budget"))
    summary = res.get("summary", {})
    if summary.get("total_income") != 2000.0 or summary.get("total_expense") != 80.0 or summary.get("balance") != 1920.0:
        print("   FAILED: Financial summary calculations are incorrect.")
        sys.exit(1)
    
    # 10. Fetch Transactions & Delete
    print("\n10. Fetch Transactions & Test Delete...")
    res = request_json("/api/transactions", headers=auth_header)
    txs = res.get("transactions", [])
    print(f"    Loaded {len(txs)} transactions.")
    
    expense_tx = next((t for t in txs if t["description"] == "API Test Lunch"), None)
    if not expense_tx:
        print("    FAILED: Created transaction was not found in transactions query.")
        sys.exit(1)
        
    tx_id = expense_tx["id"]
    print(f"    Deleting transaction ID {tx_id}...")
    res = request_json(f"/api/transactions/{tx_id}", method="DELETE", headers=auth_header)
    print("    Delete Result:", res)
    if not res.get("success"):
        print("    FAILED: Transaction deletion failed.")
        sys.exit(1)

    # 11. Verify deletion in dashboard stats
    print("\n11. Re-verifying Dashboard after Deletion...")
    res = request_json("/api/dashboard", headers=auth_header)
    summary = res.get("summary", {})
    print("    New Dashboard Stats:", summary)
    if summary.get("total_expense") != 0.0 or summary.get("balance") != 2000.0:
        print("    FAILED: Dashboard totals did not correctly update after deleting expense.")
        sys.exit(1)

    print("\n==================================================")
    print("   SUCCESS: All web API integration tests passed! ")
    print("==================================================")

if __name__ == "__main__":
    main()
