
import pytest

from ..src.app import create_app
from ..src.model.agency import Agency
from .testdata import populate


@pytest.fixture()
def app():
    yield create_app()


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def agency(app):
    agency = Agency.get_instance()
    populate(agency)
    yield agency

@pytest.fixture()
def newspaper(app):
    agency = Agency.get_instance()
    populate(agency)
    yield agency.newspapers[0]

@pytest.fixture()
def subscription(app):
    agency = Agency.get_instance()
    populate(agency)
    yield agency.subscriptions[0]

@pytest.fixture()
def editor(app):
    agency = Agency.get_instance()
    populate(agency)
    yield agency.editors[0]