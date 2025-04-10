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
