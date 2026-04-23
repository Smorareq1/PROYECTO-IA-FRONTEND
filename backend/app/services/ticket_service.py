"""
Ticket CRUD operations against SQLite.
"""
import json
import math
from datetime import datetime, timezone

from app.db.database import get_connection


def _generate_ticket_id() -> str:
    """Generate a sequential ticket ID based on the highest existing ID."""
    conn = get_connection()
    row = conn.execute(
        "SELECT MAX(CAST(SUBSTR(id, 4) AS INTEGER)) as m FROM tickets"
    ).fetchone()
    conn.close()
    num = (row["m"] or 0) + 1
    return f"TK-{num:06d}"


def create_ticket(
    subject: str,
    description: str,
    predicted_category: str,
    confidences: dict[str, float],
    created_by: str,
) -> dict:
    """Create a new ticket in the database."""
    ticket_id = _generate_ticket_id()
    now = datetime.now(timezone.utc).isoformat()

    conn = get_connection()
    conn.execute(
        """INSERT INTO tickets (id, subject, description, predicted_category, confidences,
           final_category, status, created_by, assignee_id, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, NULL, 'abierto', ?, NULL, ?, ?)""",
        (ticket_id, subject, description, predicted_category,
         json.dumps(confidences), created_by, now, now),
    )
    conn.commit()
    conn.close()

    return get_ticket(ticket_id)


def get_ticket(ticket_id: str) -> dict | None:
    """Get a single ticket by ID."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    conn.close()

    if not row:
        return None

    return _row_to_ticket(row)


def list_tickets(
    status: str | None = None,
    category: str | None = None,
    q: str | None = None,
    assignee: str | None = None,
    page: int = 1,
    size: int = 20,
) -> dict:
    """List tickets with filters and pagination."""
    conditions = []
    params = []

    if status:
        conditions.append("status = ?")
        params.append(status)
    if category:
        conditions.append("(predicted_category = ? OR final_category = ?)")
        params.extend([category, category])
    if q:
        conditions.append("(subject LIKE ? OR description LIKE ? OR id LIKE ?)")
        like = f"%{q}%"
        params.extend([like, like, like])
    if assignee:
        conditions.append("assignee_id = ?")
        params.append(assignee)

    where = " WHERE " + " AND ".join(conditions) if conditions else ""

    conn = get_connection()

    # Count total
    count_row = conn.execute(f"SELECT COUNT(*) as c FROM tickets{where}", params).fetchone()
    total = count_row["c"]

    # Fetch page
    offset = (page - 1) * size
    rows = conn.execute(
        f"SELECT * FROM tickets{where} ORDER BY created_at DESC LIMIT ? OFFSET ?",
        params + [size, offset],
    ).fetchall()
    conn.close()

    pages = math.ceil(total / size) if size > 0 else 0
    items = [_row_to_ticket(r) for r in rows]

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


def update_ticket(ticket_id: str, updates: dict) -> dict | None:
    """Update ticket fields."""
    allowed = {"status", "final_category", "assignee_id"}
    fields = {k: v for k, v in updates.items() if k in allowed and v is not None}

    if not fields:
        return get_ticket(ticket_id)

    now = datetime.now(timezone.utc).isoformat()
    fields["updated_at"] = now

    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [ticket_id]

    conn = get_connection()
    conn.execute(f"UPDATE tickets SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()

    return get_ticket(ticket_id)


def delete_ticket(ticket_id: str) -> bool:
    """Delete a ticket. Returns True if found and deleted."""
    conn = get_connection()
    cursor = conn.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def _row_to_ticket(row) -> dict:
    """Convert a sqlite3.Row to a ticket dict with parsed confidences."""
    d = dict(row)
    d["confidences"] = json.loads(d["confidences"])
    return d
