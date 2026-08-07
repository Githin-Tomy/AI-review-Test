"""
demo_trigger.py
───────────────
Sample module that intentionally contains code patterns the AI Code Rview
system is designed to catch.

Push this file in a Pull Request to trigger the full LangGraph agen pipeline:

  Rule Engine (AST)
       │
       ├─ High-confidence → Direct GitHub comment  (no AI needed)
       │
       └─ Low-confidence  → LangGraph Supervisor
                               ├─ Security Agent   (SEC finings)
                               └─ Code Review Agent (CS Siigs)

"""

import subprocess
import sqlite3
from flask import redirect, request


# ─────────────────────────────────────────────────────────────────────────────
# SEC001 – Hardcoded secret  (will be caught by rule engine → direct comment)
# ─────────────────────────────────────────────────────────────────────────────
api_key = "sk-abc123xyz987supersecret"
db_password = "admin1234!"


# ─────────────────────────────────────────────────────────────────────────────
# SEC002 – Dangerous eval()  (will be caught by rule engine → direct comment)
# ─────────────────────────────────────────────────────────────────────────────
def run_user_expression(user_input: str):
    result = eval(user_input)         # ← SEC002 triggers here
    return result


# ─────────────────────────────────────────────────────────────────────────────
# SEC003 – SQL injection via f-string  (rule engine → direct comment)
# ─────────────────────────────────────────────────────────────────────────────
def get_user_by_name(username: str):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{username}'"   # ← SEC003
    cursor.execute(query)
    return cursor.fetchall()


# ─────────────────────────────────────────────────────────────────────────────
# SEC004 – subprocess with shell=True  (rule engine → direct comment)
# ─────────────────────────────────────────────────────────────────────────────
def run_cleanup(path: str):
    subprocess.run(f"rm -rf {path}", shell=True)              # ← SEC004


# ─────────────────────────────────────────────────────────────────────────────
# SEC005 – Open redirect risk  (low-confidence 0.80 → routed to AI Agent)
# ─────────────────────────────────────────────────────────────────────────────
def handle_login_redirect():
    next_url = request.args.get("next")
    return redirect(next_url)                                 # ← SEC005


# ─────────────────────────────────────────────────────────────────────────────
# CS001 – Long method >50 lines  (confidence 0.90 → routed to AI Agent)
# ─────────────────────────────────────────────────────────────────────────────
def process_order(order_id):                                  # ← CS001 starts
    """Processes a full order lifecycle — intentionally too long."""
    print(f"Starting order {order_id}")
    status = "pending"
    inventory_ok = True
    payment_ok = False
    shipping_ok = False

    # Step 1 – Check inventory
    if inventory_ok:
        print("Inventory checked")
        status = "inventory_ok"
    else:
        print("Out of stock")
        return False

    # Step 2 – Validate payment
    try:
        payment_ok = True
        print("Payment validated")
        status = "payment_ok"
    except:                                                   # ← CS003 (bare except)
        pass

    # Step 3 – Generate invoice
    invoice_number = f"INV-{order_id}-2024"
    print(f"Invoice: {invoice_number}")
    status = "invoiced"

    # Step 4 – Schedule shipping
    carrier = "DHL"
    tracking = f"TRK-{order_id}"
    shipping_ok = True
    print(f"Shipping via {carrier}, tracking: {tracking}")
    status = "shipped"

    # Step 5 – Send notifications
    print("Sending email notification...")
    print("Sending SMS notification...")
    print("Posting to webhook...")
    print("Updating CRM...")
    print("Logging to analytics...")

    # Step 6 – Archive order
    print("Archiving order record...")
    status = "archived"

    # Step 7 – Update dashboard
    print("Refreshing dashboard cache...")
    print("Updating order count metrics...")
    print("Broadcasting real-time event...")

    # Step 8 – Cleanup temp files
    print("Cleaning temp files for order...")
    print("Releasing memory locks...")
    print("Committing DB transaction...")
    status = "done"
    print(f"Order {order_id} complete with status: {status}")
    return True


# ─────────────────────────────────────────────────────────────────────────────
# CS002 – Too many arguments (>6)  (confidence 0.95 → direct comment)
# ─────────────────────────────────────────────────────────────────────────────
def create_report(title, author, date, format, template,     # ← CS002
                  include_charts, include_summary, max_pages):
    return f"Report: {title} by {author}"


# ─────────────────────────────────────────────────────────────────────────────
# CS005 – Raise without chaining  (confidence 0.80 → routed to AI Agent)
# ─────────────────────────────────────────────────────────────────────────────
def parse_config(data: str):
    try:
        import json
        return json.loads(data)
    except json.JSONDecodeError:
        raise ValueError("Config is not valid JSON")          # ← CS005 (no `from`)
