from guardian.api.app import app

for route in app.routes:
    print(type(route).__name__, getattr(route, "path", ""))
