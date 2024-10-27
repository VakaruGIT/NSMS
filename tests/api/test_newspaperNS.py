from ..fixtures import app, client, agency
from ...src.model.issue import Issue

def test_deliver_issue(client, agency):
    # Prepare
    paper = agency.newspapers[0]
    if not paper.issues:
        issue = Issue("2022-01-01", 10, 1, 1)
        paper.add_issue(issue)
        agency.add_issue(issue)
    issue = paper.issues[0]

    assert agency.get_newspaper(paper.paper_id) is not None
    assert agency.get_issue(issue.issue_id) is not None


def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")   # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)

    # act
    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200

    assert len(agency.newspapers) == paper_count_before + 1
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14


def test_get_newspaper_information(client,agency):
    paper = agency.newspapers[0]

    response = client.get(f"/newspaper/{paper.paper_id}")  # <-- note the slash at the end!
    assert response.status_code == 200
    parsed = response.get_json()
    paper_response = parsed["newspaper"]
    assert paper_response["name"] == paper.name
    assert paper_response["frequency"] == paper.frequency
    assert paper_response["price"] == paper.price

def test_update_newspaper(client,agency):
    paper = agency.newspapers[0]

    response = client.post(f"/newspaper/{paper.paper_id}",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200

    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14

def test_delete_newspaper_by_id(client, agency):
    paper = agency.newspapers[0]
    response = client.delete(f"/newspaper/{paper.paper_id}")
    assert response.status_code == 200
    assert paper not in agency.newspapers
    parsed = response.get_json()
    expected_message = {"message": f"Newspaper with ID {paper.paper_id} was deleted"}
    assert parsed == expected_message
def test_create_issue(client, agency):
    paper = agency.newspapers[0]
    issue_count_before = len(paper.issues)

    # act
    response = client.post(f"/newspaper/{paper.paper_id}/issue", json={
        "release_date": "2020-01-01",
        "released": True,
        "page": 32,
        "editor_id": 24123
    })
    assert response.status_code == 201

    print(response.get_json())

    parsed = response.get_json()
    assert "release_date" in parsed
    assert "released" in parsed
    assert "pages" in parsed
    assert "editor" in parsed
    assert "issue_id" in parsed
    assert len(paper.issues) == issue_count_before + 1

def test_get_newspaper_issues(client, agency):
    paper = agency.newspapers[0]
    response = client.get(f"/newspaper/{paper.paper_id}/issue")
    assert response.status_code == 200
    parsed = response.get_json()
    assert len(parsed["issue newspaper"]) == len(paper.issues)

def test_get_issue_information_nonexistent_paper(client, agency):
    nonexistent_paper_id = 9999
    response = client.get(f"/newspaper/{nonexistent_paper_id}/issue/1")
    assert response.status_code == 404

def test_get_issue_information_nonexistent_issue(client, agency):
    paper_id = agency.newspapers[0].paper_id
    nonexistent_issue_id = 9999
    response = client.get(f"/newspaper/{paper_id}/issue/{nonexistent_issue_id}")
    assert response.status_code == 404

def test_list_newspaper_issues(client, agency):

  paper = agency.newspapers[0]

  response = client.get(f"/newspaper/{paper.paper_id}/issue")

  assert response.status_code == 200
  parsed = response.get_json()
  issues = parsed.get("issues", [])

def test_get_issue_information(client, agency):
    paper = agency.newspapers[0]

    response = client.get(f"/newspaper/{paper.paper_id}/issue/1")
    assert response.status_code == 200 or response.status_code == 404


def test_release_issue(client, agency):
    paper = agency.newspapers[0]
    if not paper.issues:
        paper.add_issue(Issue("2022-01-01", 10, 1, 1))
    issue = paper.issues[0]

    response = client.post(f"/newspaper/{paper.paper_id}/issue/{issue.issue_id}/release")

    assert response.status_code == 200
    parsed = response.get_json()
    assert 'issue newspaper' in parsed and parsed["issue newspaper"]["released"] == True


def test_stats_for_newspaper(client, agency):
    # Prepare
    paper, issue = agency.newspapers[0], Issue("2022-01-01", 10, 1, 1)
    paper.add_issue(issue)
    agency.add_issue(issue)

    response = client.get(f"/newspaper/{paper.paper_id}/stats")
    assert response.status_code == 200
    response_data = response.get_json()['stats newspaper']
    expected_keys = ['monthly_revenue', 'annual_revenue', 'number_subscribers']
    for key in expected_keys:
        assert key in response_data, f"Expected key '{key}' not found in the response"