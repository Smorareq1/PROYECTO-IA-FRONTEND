"""
Seed the database with demo users.
Matches the mock data emails from the frontend.
"""
from passlib.hash import bcrypt

from app.db.database import get_connection, init_db

DEMO_USERS = [
    {
        "id": "u-001",
        "email": "admin@demo.com",
        "full_name": "Ana Martínez",
        "role": "admin",
        "password": "admin123",
    },
    {
        "id": "u-002",
        "email": "agente@demo.com",
        "full_name": "Carlos López",
        "role": "agente",
        "password": "agente123",
    },
    {
        "id": "u-003",
        "email": "cliente@demo.com",
        "full_name": "María García",
        "role": "cliente",
        "password": "cliente123",
    },
]


def seed_users():
    """Insert demo users if they don't already exist."""
    init_db()
    conn = get_connection()

    for user in DEMO_USERS:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (user["email"],)
        ).fetchone()

        if existing:
            print(f"  User {user['email']} already exists, skipping.")
            continue

        password_hash = bcrypt.hash(user["password"])
        conn.execute(
            "INSERT INTO users (id, email, full_name, role, password_hash) VALUES (?, ?, ?, ?, ?)",
            (user["id"], user["email"], user["full_name"], user["role"], password_hash),
        )
        print(f"  Created user: {user['email']} (role: {user['role']})")

    conn.commit()
    conn.close()
    print("Seed complete.")


if __name__ == "__main__":
    seed_users()
