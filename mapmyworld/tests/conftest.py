# tests/conftest.py
import pytest
from mapmyworld.app_factory import create_app
from mapmyworld.app_config import configure_app
import os


os.environ["FLASK_ENV"] = "qty"

@pytest.fixture
def app():
    app = create_app("qty")
    app.config.update({"TESTING": True})
    configure_app(app)

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
