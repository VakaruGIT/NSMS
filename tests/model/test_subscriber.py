import pytest

from ...src.model.subscriber import Subscriber
from ...src.model.newspaper import Newspaper

@pytest.fixture
def subscriber():
    return Subscriber(subscriber_id=1, name="John Doe", address="123 Elm St")

def test_create_subscriber(subscriber):
    assert subscriber.name == "John Doe"
    assert subscriber.address == "123 Elm St"
    assert subscriber.subscriber_id == 1

def test_subscribe_to_newspaper(subscriber):
    newspaper = Newspaper(paper_id=1, name="Test Newspaper", frequency=7, price=3.14)
    subscriber.subscribe_to_newspaper(newspaper)
    assert subscriber.newspapers == [newspaper]

def test_serialize(subscriber):
    assert subscriber.serialize() == {
        "subscriber_id": 1,
        "name": "John Doe",
        "address": "123 Elm St",
        "newspapers": [],
        "delivered_issues": []
    }