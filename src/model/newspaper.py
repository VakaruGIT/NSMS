from typing import List

from .issue import Issue

class Newspaper(object):
    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency
        self.price: float = price
        self.issues: List[Issue] = []
        self.subscribers = []
        self.editors = []

    def add_issue(self, issue):
        self.issues.append(issue)

    def show_issues(self):
        return [issue.issue_id for issue in self.issues]

    def add_editor(self, editor):
        self.editors.append(editor)

    def add_subscriber_to_newspaper(self, subscriber):
        self.subscribers.append(subscriber)

    def deliver_issue_id_to_subscriber(self, issue, subscriber):
        issue.deliver_issue_id_to_subscriber(subscriber)

    def calculate_subscribers(self):
        return len(self.subscribers)

    def calculate_monthly_revenue(self):
        return len(self.subscribers) * self.price

    def serialize(self):
        return {
            "paper_id": self.paper_id,
            "name": self.name,
            "frequency": self.frequency,
            "price": self.price,
            "issues": [issue.issue_id for issue in self.issues],
            "subscribers": [subscriber.subscriber_id for subscriber in self.subscribers]
        }

    def serialize_paper_id(self):
        return {
            "paper_id": self.paper_id,
            "name": self.name,
            "frequency": self.frequency,
            "price": self.price
        }