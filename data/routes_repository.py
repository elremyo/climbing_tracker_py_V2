from data.supabase_client import supabase

def get_routes():
    res = (supabase
           .table("routes")
           .select("*")
           .order("grade", desc=True)
           .execute()
    )
    return res.data if res.data else []

def get_active_routes():
    """Récupère uniquement les voies non archivées"""
    res = (supabase
           .table("routes")
           .select("*")
           .eq("archived", False)
           .order("grade", desc=True)
           .execute()
    )
    return res.data if res.data else []

def add_route(name, grade, color, type=None):
    res = supabase.table("routes").insert({
        "name": name,
        "grade": grade,
        "color": color,
        "type": type,
        "archived": False  # Explicitement False par défaut
    }).execute()
    return res.data[0]

def update_route(route_id, **fields):
    res = supabase.table("routes").update(fields).eq("id", route_id).execute()
    return res.data[0] if res.data else None

def archive_route(route_id):
    """Archive une voie (soft delete)"""
    res = supabase.table("routes").update({"archived": True}).eq("id", route_id).execute()
    return res.data[0] if res.data else None

def unarchive_route(route_id):
    """Réactive une voie archivée"""
    res = supabase.table("routes").update({"archived": False}).eq("id", route_id).execute()
    return res.data[0] if res.data else None

def delete_route(route_id):
    """
    Supprime définitivement une voie.
    ⚠️ Échouera si des tentatives sont associées.
    Utilise archive_route() à la place.
    """
    try:
        supabase.table("routes").delete().eq("id", route_id).execute()
    except Exception as e:
        raise Exception(f"Impossible de supprimer : des tentatives sont associées. Utilise l'archivage à la place.")