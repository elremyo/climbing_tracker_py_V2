from pathlib import Path
from datetime import datetime
from .storage import load_json, save_json

ATTEMPTS_PATH = Path("data/attempts.json")

def get_attempts():
    return load_json(ATTEMPTS_PATH)

def add_attempt(route_id, success, notes="", attempt_date=None):
    """
    Ajoute une tentative.
    """
    attempts = get_attempts()

    # convertir attempt_date en string si c'est un date object
    if attempt_date is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    elif isinstance(attempt_date, datetime):
        date_str = attempt_date.strftime("%Y-%m-%d")
    else:
        date_str = str(attempt_date) 

    attempt = {
        "id": len(attempts) + 1,
        "route_id": route_id,
        "date": date_str,
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
            # si on passe 'attempt_date' en datetime ou string, on convertit en string
            if "attempt_date" in fields:
                d = fields.pop("attempt_date")
                if isinstance(d, datetime):
                    fields["date"] = d.strftime("%Y-%m-%d")
                else:
                    fields["date"] = str(d)
            attempt.update(fields)
            save_json(ATTEMPTS_PATH, attempts)
            return attempt
    return None

def delete_attempt(attempt_id):
    attempts = get_attempts()
    new_attempts = [a for a in attempts if a["id"] != attempt_id]
    save_json(ATTEMPTS_PATH, new_attempts)
