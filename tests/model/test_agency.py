import pytest

from ...src.model.newspaper import Newspaper
from ...src.model.editor import Editor
from ...src.model.issue import Issue
from ...src.model.subscriber import Subscriber


from ..fixtures import app, client, agency

def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1

def test_add_newspaper_same_id_should_raise_error(agency):
    # Setup: Ensure no newspaper with ID 999 exists in the agency
    existing_paper = agency.get_newspaper(999)
    if existing_paper:
        agency.remove_newspaper(existing_paper)

    # Rest of the test remains the same
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)

    # first adding of newspaper should be okay
    agency.add_newspaper(new_paper)

    new_paper2 = Newspaper(paper_id=999,
                          name="Superman Comic",
                          frequency=7,
                          price=13.14)

    with pytest.raises(ValueError, match='A newspaper with ID 999 already exists'):  # <-- this allows us to test for exceptions
        # this one should raise an exception!
        agency.add_newspaper(new_paper2)

def test_get_all_newspapers(agency):
    agency.newspapers.clear()
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == 1


def test_remove_newspaper(agency):
    agency.newspapers.clear()
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    before = len(agency.newspapers)
    agency.remove_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before - 1
    assert agency.get_newspaper(999) is None

def test_add_editor(agency):
    before = len(agency.editors)
    new_editor = Editor(editor_id=999,
                          name="John Doe",
                          address="123 Elm St")
    agency.add_editor(new_editor)
    assert len(agency.get_all_editors()) == before + 1

def test_get_editors(agency):
    agency.editors.clear()
    new_editor = Editor(editor_id=999,
                          name="John Doe",
                          address="123 Elm St")
    agency.add_editor(new_editor)
    assert len(agency.get_all_editors()) == 1

def test_get_editor_by_id(agency):
    agency.editors.clear()
    new_editor = Editor(editor_id=999,
                          name="John Doe",
                          address="123 Elm St")
    agency.add_editor(new_editor)
    assert agency.get_editor(999) == new_editor
def test_remove_editor(agency):
    agency.editors.clear()
    new_editor = Editor(editor_id=999,
                          name="John Doe",
                          address="123 Elm St")
    agency.add_editor(new_editor)
    before = len(agency.editors)
    agency.remove_editor(new_editor)
    assert len(agency.get_all_editors()) == before - 1
    assert agency.get_editor(999) is None

def test_add_issue(agency):
    before = len(agency.issues)
    new_issue = Issue(releasedate="2021-01-01",
                      page=1,
                      editor=1,
                      issue_id=1)
    agency.add_issue(new_issue)
    assert len(agency.issues) == before + 1

def test_get_issue(agency):
    agency.issues.clear()
    new_issue = Issue(releasedate="2021-01-01",
                      page=1,
                      editor=1,
                      issue_id=1)
    agency.add_issue(new_issue)
    assert agency.get_issue(1) == new_issue

def test_add_subscriber(agency):
    before = len(agency.subscriber)
    new_subscriber = Subscriber(subscriber_id=999,
                          name="John Doe",
                          address="123 Elm St")

    agency.add_subscriber(new_subscriber)
    assert len(agency.all_subscribers()) == before + 1

def test_get_subscriber(agency):
    agency.subscriber.clear()
    new_subscriber = Subscriber(subscriber_id=999,
                          name="John Doe",
                          address="123 Elm St")
    agency.add_subscriber(new_subscriber)
    assert agency.get_subscriber(999) == new_subscriber


def test_remove_subscriber(agency):
    agency.subscriber.clear()
    new_subscriber = Subscriber(subscriber_id=999,
                          name="John Doe",
                          address="123 Elm St")
    agency.add_subscriber(new_subscriber)
    before = len(agency.subscriber)
    agency.remove_subscriber(new_subscriber)
    assert len(agency.all_subscribers()) == before - 1
    assert agency.get_subscriber(999) is None

def test_get_all_subscribers(agency):
    agency.subscriber.clear()
    new_subscriber = Subscriber(subscriber_id=999,
                          name="John Doe",
                          address="123 Elm St")
    agency.add_subscriber(new_subscriber)
    assert len(agency.all_subscribers()) == 1