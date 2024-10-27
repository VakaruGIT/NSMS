import pytest

from ...src.model.issue import Issue
from ...src.model.subscriber import Subscriber

@pytest.fixture
def issue():
    return Issue(issue_id=1, releasedate="2021-01-01", page=1, editor=1)

def test_set_editor(issue):
    issue.set_editor(999)
    assert issue.editor_id == 999

def test_get_issue_by_id(issue):
    assert issue.get_issue_by_id(1) == 1

def test_deliver_issue_id_to_subscriber(issue):
    new_subscriber = Subscriber(subscriber_id=999,
                                name="John Doe",
                                address="123 Elm St")
    issue.deliver_issue_id_to_subscriber(new_subscriber)
    assert new_subscriber in issue.subscribers

def test_serialize(issue):
    assert issue.serialize() == {
        "issue_id": 1,
        "release_date": "2021-01-01",
        "pages": 1,
        "editor": 1,
        "released": False,
        "subscribers": []
    }