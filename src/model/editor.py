from typing import List
from .newspaper import Newspaper

class Editor(object):
    def __init__(self, editor_id: int, name: str, address: str):
        self.editor_id: int = editor_id
        self.name: str = name
        self.address: str = address
        self.newspapers: List[Newspaper] = []

    def assign_issue(self, issue, newspaper):
        # Ensure this editor is linked to the newspaper
        if newspaper not in self.newspapers:
            self.newspapers.append(newspaper)
        # Link the issue to the newspaper; this assumes the Newspaper class has a method to handle this
        newspaper.add_issue(issue)

    def get_editor_issues_ids(self):
        # return the paper_id of each newspaper in the list of newspapers
        newspaper_ids = [newspaper.paper_id for newspaper in self.newspapers]
        return newspaper_ids

    def reassign_issue(self, issue, other_editor):
        self.newspapers.remove(issue.newspaper)
        other_editor.assign_issue(issue, issue.newspaper)
    def serialize(self):
        return {
            "editor_id": self.editor_id,
            "name": self.name,
            "address": self.address,
            "newspapers": [newspaper.paper_id for newspaper in self.newspapers]
        }