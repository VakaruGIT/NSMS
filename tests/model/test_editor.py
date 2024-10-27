import pytest
from ...src.model.newspaper import Newspaper
from ...src.model.issue import Issue
from ...src.model.editor import Editor

@pytest.fixture
def editor():
    return Editor(editor_id=1, name="John Doe", address="123 Elm St")

def test_assign_issue(editor):
    newspaper = Newspaper(paper_id=1, name="Test Newspaper", frequency=7, price=3.14)
    issue = Issue(issue_id=1, releasedate="2021-01-01", page=1, editor=editor)
    editor.assign_issue(issue, newspaper)
    assert newspaper.issues == [issue]
    assert editor.newspapers == [newspaper]

def test_show_editor_issues(editor):
    newspaper = Newspaper(paper_id=1, name="Test Newspaper", frequency=7, price=3.14)
    issue = Issue(issue_id=1, releasedate="2021-01-01", page=1, editor=editor)
    editor.assign_issue(issue, newspaper)
    assert editor.get_editor_issues_ids() == [1]

def test_serialize(editor):
    assert editor.serialize() == {
        "editor_id": 1,
        "name": "John Doe",
        "address": "123 Elm St",
        "newspapers": []
   }

