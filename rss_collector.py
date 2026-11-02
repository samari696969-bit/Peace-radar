"""Fetch only feeds explicitly listed in sources.json.

Each source entry must define:
  name, url, region, status
Use official public feeds. This collector does not infer locations or coordinates.
"""
import hashlib
import time
import feedparser
from config import load_sources
from database import init_db, add_event

def clean(value, limit=1200):
    return " ".join((value or "").split())[:limit]

def run_once():
    init_db()
    total = 0
    for source in load_sources():
        required = ("name", "url", "region", "status")
        if not all(source.get(k) for k in required):
            print("Skipping incomplete source:", source.get("name", "unnamed"))
            continue
        feed = feedparser.parse(source["url"])
        for entry in feed.entries:
            title = clean(entry.get("title"), 300)
            link = entry.get("link", "")
            summary = clean(entry.get("summary"), 1200)
            published = entry.get("published", entry.get("updated", ""))
            if not title:
                continue
            fingerprint = hashlib.sha256((source["name"] + "|" + link + "|" + title).encode()).hexdigest()
            if add_event(source["name"], link, title, summary, source["region"],
                         source["status"], published, fingerprint):
                total += 1
    print(f"Added {total} new public notices")
    return total

if __name__ == "__main__":
    run_once()
