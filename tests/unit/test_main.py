import pytest
from fastapi import FastAPI

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


