import pytest
from fastapi import FastAPI

from tests.helpers import load_test_data_file 

from main import app


pytestmark = [
    pytest.mark.unit,
    pytest.mark.api
]


def test_app_is_fastapi_instance():
    assert isinstance(app, FastAPI)


def test_app_title():
    assert app.title == "Finance Tracker API"


def test_app_version(api_version):
    assert app.version == api_version


def test_api_prefix(api_prefix):
    for route in app.routes:
        if route.path not in ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]:
            assert route.path.startswith(api_prefix)


def test_api_routes(api_prefix):
    loaded_routes = load_test_data_file("api/test_included_api_routes.json")
    valid_routes = {}
    for method, list_of_routes in loaded_routes.items():
        for route in list_of_routes:
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