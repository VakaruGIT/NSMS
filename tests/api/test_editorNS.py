from ..fixtures import app, client, agency

from ...src.model.issue import Issue
from ...src.model.editor import Editor


def test_issue_initialization_with_valid_parameters():
    issue = Issue("2022-01-01", 10, 1, 1)
    assert issue.release_date == "2022-01-01"
    assert issue.page == 10
    assert issue.editor_id == 1
    assert issue.issue_id == 1
    assert not issue.released


def test_issue_initialization_with_released_status():
    issue = Issue("2022-01-01", 10, 1, 1, True)
    assert issue.release_date == "2022-01-01"
    assert issue.page == 10
    assert issue.editor_id == 1
    assert issue.issue_id == 1
    assert issue.released

def test_issue_set_editor():
    issue = Issue("2022-01-01", 10, 1, 1)
    issue.set_editor(5)
    assert issue.editor_id == 5

def test_issue_get_issue_by_id():
    issue = Issue("2022-01-01", 10, 1, 1)
    assert issue.get_issue_by_id(1) == 1

def test_issue_serialize():
    issue = Issue("2022-01-01", 10, 1, 1)
    serialized = issue.serialize()
    assert serialized["issue_id"] == 1
    assert serialized["release_date"] == "2022-01-01"
    assert serialized["pages"] == 10
    assert serialized["editor"] == 1
    assert not serialized["released"]


def test_editor_creation_with_missing_data(client):
    response = client.post("/editor/", json={"name": "John Doe"})
    assert response.status_code == 500

def test_editor_retrieval_with_invalid_id(client):
    invalid_editor_id = 9999
    response = client.get(f"/editor/{invalid_editor_id}")
    assert response.status_code == 200

def test_create_editor(client, agency):
    response = client.post("/editor/", json={"name": "John Doe", "address": "1234 Elm Street"})
    assert response.status_code == 200

def test_get_all_editors(client, agency):
    response = client.get("/editor/")
    assert response.status_code == 200

def test_get_editor_information(client, agency):
    response = client.get("/editor/1")
    assert response.status_code == 200

def test_update_editor_information(client, agency):
    # Ensure an editor with id 1 exists in the agency
    agency.add_editor(Editor(1, "John Doe", "1234 Elm Street"))

    response = client.post("/editor/1", json={"name": "Jane Doe"})
    assert response.status_code == 200


def test_delete_editor(client, agency):
    # Ensure an editor with id 1 exists in the agency
    agency.add_editor(Editor(1, "John Doe", "1234 Elm Street"))

    editor = agency.get_editor(1)
    if editor:
        response = client.delete("/editor/1")
        print(response.data)
        assert response.status_code == 200
    else:
        print("Editor with ID 1 does not exist.")

def test_editor_initialization_with_valid_parameters():
    editor = Editor(1, "John Doe", "1234 Elm Street")
    assert editor.editor_id == 1
    assert editor.name == "John Doe"
    assert editor.address == "1234 Elm Street"

def test_show_editor_issues():
    editor = Editor(1, "John Doe", "1234 Elm Street")
    assert editor.get_editor_issues_ids() == []