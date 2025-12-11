from .supabase_client import supabase

def get_routes():
    res = (supabase
           .table("routes")
           .select("*")
           .order("grade", desc=True)
           .execute()
    )
    return res.data if res.data else []

def add_route(name, grade, color):
    res = supabase.table("routes").insert({
        "name": name,
        "grade": grade,
        "color": color
    }).execute()
    return res.data[0]

def update_route(route_id, **fields):
    res = supabase.table("routes").update(fields).eq("id", route_id).execute()
    return res.data[0] if res.data else None

def delete_route(route_id):
    supabase.table("routes").delete().eq("id", route_id).execute()
