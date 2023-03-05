import pytest
from flask.testing import FlaskClient

from flask_app.app import app
from server.database import Database
from server.model import Task


@pytest.fixture(scope="session")
def database() -> Database:
    return Database(url="sqlite:///db.test.sqlite")


@pytest.fixture(scope="session")
def client(database: Database) -> FlaskClient:
    app.set_database(database)
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def task1(database: Database) -> Task:
    return Task("Task 1", database)
