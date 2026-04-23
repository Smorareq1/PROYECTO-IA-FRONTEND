"""
SQLite database using Python stdlib sqlite3. No ORM.
"""
import sqlite3
from pathlib import Path

from app.config import DATABASE_PATH

# SQL schema
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('cliente', 'agente', 'admin')),
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tickets (
    id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    predicted_category TEXT NOT NULL,
    confidences TEXT NOT NULL,
    final_category TEXT,
    status TEXT NOT NULL DEFAULT 'abierto'
        CHECK(status IN ('abierto', 'en_progreso', 'resuelto', 'cerrado')),
    created_by TEXT NOT NULL,
    assignee_id TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (assignee_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(predicted_category);
CREATE INDEX IF NOT EXISTS idx_tickets_created_by ON tickets(created_by);
CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee_id);
"""


def get_connection() -> sqlite3.Connection:
    """Get a SQLite connection with row_factory for dict-like access."""
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
