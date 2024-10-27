from typing import List
from .newspaper import Newspaper
from .issue import Issue

class Subscriber(object):
    def __init__(self,subscriber_id: int, name: str, address: str):
        self.subscriber_id: int = subscriber_id
        self.name: str = name
        self.address: str = address
        self.newspapers: List[Newspaper] = []
        self.delivered_issues: List[Issue] = []

    def create_subscriber(self, subscriber_id: int, name: str, address: str):
        return Subscriber(subscriber_id, name, address)

    def subscribe_to_newspaper(self, newspaper: Newspaper):
        if newspaper not in self.newspapers:
            self.newspapers.append(newspaper)
        newspaper.add_subscriber_to_newspaper(self)

    def serialize(self):
        return {
            "subscriber_id": self.subscriber_id,
            "name": self.name,
            "address": self.address,
            "newspapers": [newspaper.serialize() for newspaper in self.newspapers],
            "delivered_issues": [issue.serialize() for issue in self.delivered_issues]
        }

    def calculate_subscriptions(self):
        return len(self.newspapers)

    def calculate_monthly_cost(self):
        return sum([newspaper.price for newspaper in self.newspapers])

    def calculate_issues(self):
        return len(self.delivered_issues)

    def serialize_subscriber_id(self):
        return {
            "subscriber_id": self.subscriber_id,
            "name": self.name,
            "address": self.address}