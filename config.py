import json
from pathlib import Path

def load_sources():
    path = Path("sources.json")
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))
