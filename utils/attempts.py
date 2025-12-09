from pathlib import Path
from datetime import datetime
from .storage import load_json, save_json

ATTEMPTS_PATH = Path("data/attempts.json")

def get_attempts():
    return load_json(ATTEMPTS_PATH)

def add_attempt(route_id, success, notes=""):
    attempts = get_attempts()

    attempt = {
        "id": len(attempts) + 1,
        "route_id": route_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "success": success,
        "notes": notes
    }

    attempts.append(attempt)
    save_json(ATTEMPTS_PATH, attempts)
    return attempt

def update_attempt(attempt_id, **fields):
    attempts = get_attempts()
    for attempt in attempts:
        if attempt["id"] == attempt_id:
            attempt.update(fields)
            save_json(ATTEMPTS_PATH, attempts)
            return attempt
    return None

def delete_attempt(attempt_id):
    attempts = get_attempts()
    new_attempts = [a for a in attempts if a["id"] != attempt_id]
    save_json(ATTEMPTS_PATH, new_attempts)
