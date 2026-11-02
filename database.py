import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.getenv("DATABASE_PATH", "peace_radar.db")

def connect():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with connect() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            source_url TEXT,
            title TEXT NOT NULL,
            summary TEXT,
            region TEXT NOT NULL,
            status TEXT NOT NULL,
            published_at TEXT,
            created_at TEXT NOT NULL,
            fingerprint TEXT UNIQUE
        )
        """)

def add_event(source, source_url, title, summary, region, status, published_at, fingerprint):
    now = datetime.now(timezone.utc).isoformat()
    with connect() as db:
        cur = db.execute("""
        INSERT OR IGNORE INTO events
        (source, source_url, title, summary, region, status, published_at, created_at, fingerprint)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (source, source_url, title, summary, region, status, published_at, now, fingerprint))
        return cur.rowcount == 1

def get_events(limit=100):
    with connect() as db:
        rows = db.execute("""
        SELECT id, source, source_url, title, summary, region, status, published_at
        FROM events ORDER BY COALESCE(published_at, created_at) DESC LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]

def get_region_status():
    with connect() as db:
        rows = db.execute("""
        SELECT region, status, title, source, source_url, published_at
        FROM events e
        WHERE id = (SELECT id FROM events x WHERE x.region=e.region
                    ORDER BY COALESCE(x.published_at,x.created_at) DESC LIMIT 1)
        ORDER BY region
        """).fetchall()
        return [dict(r) for r in rows]
