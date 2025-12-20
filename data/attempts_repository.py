from data.supabase_client import supabase
from services.user_context import UserContext

def get_attempts():
    """
    Récupère toutes les tentatives de l'utilisateur connecté, triées par date décroissante.
    """
    user_id = UserContext.get_user_id()
    if not user_id:
        return []
    
    res = (
        supabase
        .table("attempts")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data if res.data else []


def add_attempt(route_id, success, notes="", attempt_date=None):
    """Ajoute une tentative pour l'utilisateur connecté"""
    user_id = UserContext.get_user_id()
    if not user_id:
        raise Exception("Utilisateur non connecté")
    
    # convertir datetime.date en string "YYYY-MM-DD" si nécessaire
    if attempt_date is None:
        date_str = None  
    elif hasattr(attempt_date, "isoformat"):
        date_str = attempt_date.isoformat() 
    else:
        date_str = str(attempt_date)

    data = {
        "route_id": route_id,
        "success": success,
        "notes": notes,
        "date": date_str,
        "user_id": user_id
    }

    res = supabase.table("attempts").insert(data).execute()
    return res.data[0]

def update_attempt(attempt_id, route_id, success, notes="", attempt_date=None):
    """Met à jour une tentative (vérifié par RLS)"""
    # convertir datetime.date en string "YYYY-MM-DD" si nécessaire
    if attempt_date is None:
        date_str = None 
    elif hasattr(attempt_date, "isoformat"):
        date_str = attempt_date.isoformat() 
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
    """Supprime une tentative (vérifié par RLS)"""
    res = supabase.table("attempts").delete().eq("id", attempt_id).execute()
    return res.data