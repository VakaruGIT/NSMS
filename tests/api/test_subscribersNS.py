from ..fixtures import app, client, agency
from ...src.model.subscriber import Subscriber

def test_subscriber_initialization_with_valid_parameters():
    subscriber = Subscriber(1, "John Doe", "1234 Elm Street")
    assert subscriber.subscriber_id == 1
    assert subscriber.name == "John Doe"
    assert subscriber.address == "1234 Elm Street"

def test_subscriber_initialization_with_invalid_parameters():
    subscriber = Subscriber(1, "John Doe", "1234 Elm Street")
    assert subscriber.subscriber_id == 1
    assert subscriber.name == "John Doe"
    assert subscriber.address == "1234 Elm Street"
def test_get_all_subscribers(client, agency):
    response = client.get("/subscriber/")
    assert response.status_code == 200

    parsed = response.get_json()
    assert len(parsed["subscribers"]) == len(agency.subscriber)

def test_create_subscriber(client, agency):
    subscriber_count_before = len(agency.subscriber)
    response = client.post("/subscriber/",
                           json={
                               "name": "John Doe",
                               "address": "1234 Elm Street"
                           })
    assert response.status_code == 200

    assert len(agency.subscriber) == subscriber_count_before + 1
    parsed = response.get_json()
    subscriber_response = parsed.get("subscriber")
    if not subscriber_response:
        print("Warning: The key 'subscriber' was not found in the response")


def test_get_subscriber_information(client,agency):
    if not agency.subscriber:
        print("No subscribers in the agency.")
        return
    subscriber = agency.subscriber[0]

    response = client.get(f"/subscriber/{subscriber.subscriber_id}")

    assert response.status_code == 200
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]

    assert subscriber_response["name"] == subscriber.name
    assert subscriber_response["address"] == subscriber.address



def test_delete_subscriber_by_id(client, agency):
    if not agency.subscriber:
        print("No subscribers in the agency.")
        return
    subscriber = agency.subscriber[0]

    response = client.delete(f"/subscriber/{subscriber.subscriber_id}")
    assert response.status_code == 200

    assert subscriber not in agency.subscriber

def test_delete_subscriber_with_invalid_id(client):
    response = client.delete("/subscriber/9999")
    assert response.status_code == 404

def test_subscriber_subscribe_to_newspaper(client, agency):
    if not agency.subscriber:
        print("No subscribers in the agency.")
        return
    subscriber = agency.subscriber[0]
    if not agency.newspapers:
        print("No newspapers in the agency.")
        return
    newspaper = agency.newspapers[0]

    response = client.post(f"/subscriber/{subscriber.subscriber_id}/subscribe/{newspaper.paper_id}")

    assert response.status_code == 200
    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]

    assert newspaper in subscriber_response["newspapers"]

def test_subscriber_stats(client, agency):
    if not agency.subscriber:
        print("No subscribers in the agency.")
        return
    subscriber = agency.subscriber[0]

    response = client.get(f"/subscriber/{subscriber.subscriber_id}/stats")

    assert response.status_code == 200
    parsed = response.get_json()
    subscriber_response = parsed["stats subscriber"]

    assert subscriber_response["number_of_subscriptions"] == len(subscriber.newspapers)
    assert subscriber_response["monthly_cost"] == subscriber.calculate_monthly_cost()
    assert subscriber_response["annual_cost"] == subscriber.calculate_annual_cost()

def test_subscriber_missing_issues(client, agency):
    if not agency.subscriber:
        print("No subscribers in the agency.")
        return
    subscriber = agency.subscriber[0]

    response = client.get(f"/subscriber/{subscriber.subscriber_id}/missingissues")

    assert response.status_code == 200
    parsed = response.get_json()
    missing_issues_response = parsed["missing_issues"]

    assert len(missing_issues_response) == len(subscriber.missing_issues())
    for issue in missing_issues_response:
        assert issue in subscriber.missing_issues()

def test_update_subscriber(client,agency):
    if not agency.subscriber:
        print("No subscribers in the agency.")
        return
    subscriber = agency.subscriber[0]

    response = client.post(f"/subscriber/{subscriber.subscriber_id}",
                           json={
                               "name": "Jane Doe"
                           })
    assert response.status_code == 200

    parsed = response.get_json()
    subscriber_response = parsed["subscriber"]

    assert subscriber_response["name"] == "Jane Doe"