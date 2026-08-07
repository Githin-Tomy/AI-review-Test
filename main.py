"""
Fixture: pr_002_sql_injection

Injected issue:
- SQL query built with f-string → SEC003 Critical

Expected finding:
- SEC003 (confidence ≥ 95% → direct publish)
"""

import sqlite3
from typing import Optional


def get_user_by_username(username: str) -> Optional[dict]:
    """Retrieve a user record by username."""

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # ✅ GOOD: Parameterized query
    cursor.execute(
        "SELECT id, username, email FROM users WHERE username = ?",
        (username,),
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
        }

    return None


def delete_user(user_id: str) -> bool:
    """Delete a user by ID."""

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # ✅ GOOD: Parameterized query
    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,),
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted



def search_products(search_term: str, limit: int) -> list:
    """Search products by name with a strict limit."""

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    # ✅ GOOD: Parameterized query
    cursor.execute(
        "SELECT * FROM products WHERE name LIKE ? LIMIT ?",
        (f"%{search_term}%", limit),
    )

    results = cursor.fetchall()

    conn.close()

    return results