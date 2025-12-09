from pathlib import Path
from .storage import load_json, save_json

ROUTES_PATH = Path("data/routes.json")

def get_routes():
    return load_json(ROUTES_PATH)

def add_route(name, grade, color):
    routes = get_routes()
    new_id = max([r["id"] for r in routes], default=0) + 1

    route = {
        "id": new_id,
        "name": name,
        "grade": grade,
        "color": color,
        "archived": False
    }

    routes.append(route)
    save_json(ROUTES_PATH, routes)
    return route

def update_route(route_id, **fields):
    routes = get_routes()
    for route in routes:
        if route["id"] == route_id:
            route.update(fields)
            save_json(ROUTES_PATH, routes)
            return route
    return None

def delete_route(route_id):
    routes = get_routes()
    new_routes = [r for r in routes if r["id"] != route_id]
    save_json(ROUTES_PATH, new_routes)

def archive_route(route_id):
    return update_route(route_id, archived=True)
