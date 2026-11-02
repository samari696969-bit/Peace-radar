"""Small validation helper for sources.json."""
from config import load_sources

ALLOWED_STATUS = {"info", "warning", "all_clear", "unknown"}

def validate():
    for item in load_sources():
        if item.get("status") not in ALLOWED_STATUS:
            raise ValueError(f"Unsupported status for {item.get('name')}")
        if not item.get("url", "").startswith("https://"):
            raise ValueError(f"Feed must use HTTPS: {item.get('name')}")
    print("Source configuration looks valid.")

if __name__ == "__main__":
    validate()
