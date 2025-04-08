import pytest
from fastapi import FastAPI
from app.core.setup_app import create_app

def test_create_app_returns_fastapi_instance():
    app = create_app()
    assert isinstance(app, FastAPI)

def test_create_app_title():
    app = create_app()
    assert app.title == "Finance Tracker API"
