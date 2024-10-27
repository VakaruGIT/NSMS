import pytest
from ...src.model.newspaper import Newspaper
from ...src.model.issue import Issue
from ...src.model.editor import Editor
from ...src.model.subscriber import Subscriber
@pytest.fixture
def newspaper():
    return Newspaper(paper_id=1, name="Test Newspaper", frequency=7, price=3.14)

def test_add_issue(newspaper):
    before = len(newspaper.issues)
    new_issue = Issue(issue_id=999,
                      releasedate="2021-01-01",
                      page=1,
                      editor=1)
    newspaper.add_issue(new_issue)
    assert len(newspaper.issues) == before + 1

def test_show_issues(newspaper):
    newspaper.issues.clear()
    new_issue = Issue(issue_id=999,
                      releasedate="2021-01-01",
                      page=1,
                      editor=1)
    newspaper.add_issue(new_issue)
    assert newspaper.show_issues() == [999]

def test_add_editor(newspaper):
    before = len(newspaper.editors)
    new_editor = Editor(editor_id=999,
                        name="John Doe",
                        address="123 Elm St")
    newspaper.add_editor(new_editor)
    assert len(newspaper.editors) == before + 1

def test_add_subscriber_to_newspaper(newspaper):
    before = len(newspaper.subscribers)
    new_subscriber = Subscriber(subscriber_id=999,
                                name="John Doe",
                                address="123 Elm St")
    newspaper.add_subscriber_to_newspaper(new_subscriber)
    assert len(newspaper.subscribers) == before + 1

def test_deliver_issue_id_to_subscriber(newspaper):
    new_subscriber = Subscriber(subscriber_id=999,
                                name="John Doe",
                                address="123 Elm St")
    new_issue = Issue(issue_id=999,
                      releasedate="2021-01-01",
                      page=1,
                      editor=1)
    newspaper.add_issue(new_issue)
    newspaper.deliver_issue_id_to_subscriber(new_issue, new_subscriber)
    assert new_subscriber in new_issue.subscribers

def test_calculate_subscribers(newspaper):
    new_subscriber = Subscriber(subscriber_id=999,
                                name="John Doe",
                                address="123 Elm St")
    newspaper.add_subscriber_to_newspaper(new_subscriber)
    assert newspaper.calculate_subscribers() == 1

def test_calculate_monthly_revenue(newspaper):
    new_subscriber = Subscriber(subscriber_id=999,
                                name="John Doe",
                                address="123 Elm St")
    newspaper.add_subscriber_to_newspaper(new_subscriber)
    assert newspaper.calculate_monthly_revenue() == 3.14

def test_serialize(newspaper):
    new_issue = Issue(issue_id=999,
                      releasedate="2021-01-01",
                      page=1,
                      editor=1)
    newspaper.add_issue(new_issue)
    new_subscriber = Subscriber(subscriber_id=999,
                                name="John Doe",
                                address="123 Elm St")
    newspaper.add_subscriber_to_newspaper(new_subscriber)
    assert newspaper.serialize() == {
        "paper_id": 1,
        "name": "Test Newspaper",
        "frequency": 7,
        "price": 3.14,
        "issues": [999],
        "subscribers": [999]
    }