from .supabase_client import supabase

def get_attempts():
    """
    Récupère toutes les tentatives, triées par date décroissante.
    """
    res = (
        supabase
        .table("attempts")
        .select("*")
        .order("date", desc=True)
        .execute()
    )
    # res.data est une liste de dict
    return res.data if res.data else []


def add_attempt(route_id, success, notes="", attempt_date=None):
    # convertir datetime.date en string "YYYY-MM-DD" si nécessaire
    if attempt_date is None:
        date_str = None  # ou mettre datetime.now().strftime("%Y-%m-%d")
    elif hasattr(attempt_date, "isoformat"):
        date_str = attempt_date.isoformat()  # date -> "YYYY-MM-DD"
    else:
        date_str = str(attempt_date)

    data = {
        "route_id": route_id,
        "success": success,
        "notes": notes,
        "date": date_str
    }

    res = supabase.table("attempts").insert(data).execute()
    return res.data[0]

def update_attempt(attempt_id, route_id, success, notes="", attempt_date=None):
    # convertir datetime.date en string "YYYY-MM-DD" si nécessaire
    if attempt_date is None:
        date_str = None  # ou mettre datetime.now().strftime("%Y-%m-%d")
    elif hasattr(attempt_date, "isoformat"):
        date_str = attempt_date.isoformat()  # date -> "YYYY-MM-DD"
    else:
        date_str = str(attempt_date)

    data = {
        "route_id": route_id,
        "success": success,
        "notes": notes,
        "date": date_str
    }

    res = supabase.table("attempts").update(data).eq("id", attempt_id).execute()
    return res.data[0]

def delete_attempt(attempt_id):
    res = supabase.table("attempts").delete().eq("id", attempt_id).execute()
    return res.data
