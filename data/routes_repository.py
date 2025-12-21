from data.supabase_client import supabase
from services.user_context import UserContext

def get_routes():
    """Récupère toutes les voies de l'utilisateur connecté"""
    user_id = UserContext.get_user_id()
    if not user_id:
        return []
    
    res = (supabase
           .table("routes")
           .select("*")
           .eq("user_id", user_id)
           .order("grade", desc=True)
           .execute()
    )
    return res.data if res.data else []

def get_active_routes():
    """Récupère uniquement les voies de l'utilisateur"""
    user_id = UserContext.get_user_id()
    if not user_id:
        return []
    
    res = (supabase
           .table("routes")
           .select("*")
           .eq("user_id", user_id)
           .order("grade", desc=True)
           .execute()
    )
    return res.data if res.data else []

def add_route(name, grade, color):
    """Ajoute une voie pour l'utilisateur connecté"""
    user_id = UserContext.get_user_id()
    if not user_id:
        raise Exception("Utilisateur non connecté")
    
    res = supabase.table("routes").insert({
        "name": name,
        "grade": grade,
        "color": color,
        "user_id": user_id
    }).execute()
    return res.data[0]

def update_route(route_id, **fields):
    """Met à jour une voie (vérifié par RLS)"""
    res = supabase.table("routes").update(fields).eq("id", route_id).execute()
    return res.data[0] if res.data else None