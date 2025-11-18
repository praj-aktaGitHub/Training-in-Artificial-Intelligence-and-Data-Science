# ticketing_agent.py
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
import os


DB_PATH = "tickets.db"


# -------------------------------------------------------------------
# Initialize DB automatically (runs once)
# -------------------------------------------------------------------
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE tickets (
                ticket_id TEXT PRIMARY KEY,
                user_query TEXT,
                troubleshooting_steps TEXT,
                convo_id TEXT,
                created_at TEXT,
                status TEXT,
                extra_meta TEXT
            )
        """)
        conn.commit()
        conn.close()

init_db()


# -------------------------------------------------------------------
# Utility for DB execution
# -------------------------------------------------------------------
def db_execute(query: str, params=()):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()


def db_fetch(query: str, params=()):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows


# -------------------------------------------------------------------
# Ticketing Agent — used inside LangGraph
# -------------------------------------------------------------------
class TicketingAgent:
    """
    Stores tickets in SQLite.
    Called by your LangGraph ticket_node.
    """

    def __init__(self):
        pass

    def create_ticket(
        self,
        user_query: str,
        troubleshooting_steps: List[str],
        meta: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create + store a ticket in SQLite.
        """

        ticket_id = f"TKT-{uuid.uuid4().hex[:8]}"
        created_at = datetime.utcnow().isoformat()

        # convert troubleshooting steps into multiline text
        steps_text = "\n".join(troubleshooting_steps)

        # meta → stored as simple str (convert dict to str)
        extra_meta = str(meta)

        db_execute("""
            INSERT INTO tickets (ticket_id, user_query, troubleshooting_steps, convo_id, created_at, status, extra_meta)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_id,
            user_query,
            steps_text,
            meta.get("convo_id"),
            created_at,
            "open",
            extra_meta
        ))

        return {
            "ticket_id": ticket_id,
            "user_query": user_query,
            "steps": troubleshooting_steps,
            "convo_id": meta.get("convo_id"),
            "created_at": created_at,
            "status": "open",
            "meta": meta
        }

    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        rows = db_fetch("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
        if not rows:
            return None
        row = rows[0]
        return {
            "ticket_id": row[0],
            "user_query": row[1],
            "troubleshooting_steps": row[2],
            "convo_id": row[3],
            "created_at": row[4],
            "status": row[5],
            "extra_meta": row[6]
        }

    def update_status(self, ticket_id: str, new_status: str):
        db_execute(
            "UPDATE tickets SET status=? WHERE ticket_id=?",
            (new_status, ticket_id)
        )

    def list_tickets(self) -> List[Dict]:
        rows = db_fetch("SELECT * FROM tickets ORDER BY created_at DESC")
        return [
            {
                "ticket_id": r[0],
                "user_query": r[1],
                "troubleshooting_steps": r[2],
                "convo_id": r[3],
                "created_at": r[4],
                "status": r[5],
                "extra_meta": r[6]
            }
            for r in rows
        ]
