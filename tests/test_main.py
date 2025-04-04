from main import app
from app.config import APP_CFG
from tests.helpers.read_test_data import load_test_data_file

API_PREFIX = f"/api/{APP_CFG['API_VERSION']}"

def test_app_title_and_version():
    assert app.title == "Finance Tracker API"
    assert app.version == APP_CFG["API_VERSION"]

def test_api_version_prefix():
    for route in app.routes:
        if route.path not in ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]:
            assert route.path.startswith(API_PREFIX)

def test_api_routes():
    loaded_routes = load_test_data_file("test_main_routes.json")
    valid_routes = {}
    for method, list_of_routes in loaded_routes.items():
        for route in list_of_routes:
            route = API_PREFIX + route
            if method not in valid_routes:
                valid_routes[method] = [route]
            else: 
                valid_routes[method].append(route)

    app_methods = []
    app_routes = {}
    for route in app.routes:
        if route.path not in ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]:
            for method in list(route.methods):
                if method not in app_methods:
                    app_methods.append(method)
    
    for route in app.routes:
        if route.path not in ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]:
            for method in list(route.methods):
                if method not in app_routes:
                    app_routes[method] = []
                app_routes[method].append(route.path)
    
    assert app_routes == valid_routes
