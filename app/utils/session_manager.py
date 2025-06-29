import json
import os

STORAGE_FILE = "sessions.json"

if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "r") as f:
        content = f.read().strip()
        if content:
            SESSIONS = json.loads(content)
        else:
            SESSIONS = {}
else:
    SESSIONS = {}

def save_sessions():
    with open(STORAGE_FILE, "w") as f:
        json.dump(SESSIONS, f, indent=2)
