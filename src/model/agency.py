from typing import List, Union, Optional

from .newspaper import Newspaper
from .editor import Editor
from .subscriber import Subscriber
from .issue import Issue


class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
        self.subscriber: List[Subscriber] = []
        self.issues: List[Issue] = []


    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance
# Newspaper related methods
    def add_newspaper(self, new_paper: Newspaper, paper_id: int = None):
        if any(existing_newspaper.paper_id == new_paper.paper_id for existing_newspaper in self.newspapers):
            raise ValueError(f'A newspaper with ID {new_paper.paper_id} already exists')
        self.newspapers.append(new_paper)

    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers


    def remove_newspaper(self, paper: Newspaper):
        for paper in self.newspapers:
            if paper.paper_id == paper.paper_id:
                self.newspapers.remove(paper)
# Editor related methods
    def add_editor(self, new_editor: Editor):
        self.editors.append(new_editor)

    def get_editor(self, editor_id: Union[int,str]) -> Optional[Editor]:
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return None

    def remove_editor(self, editor: Editor):
        for editor in self.editors:
            if editor.editor_id == editor.editor_id:
                self.editors.remove(editor)

# Issue related methods
    def add_issue(self,new_issue: Issue, issue_id: int = None):
        self.issue_id = issue_id
        self.issues.append(new_issue)

    def get_all_editors(self) -> List[Editor]:
        return self.editors

    def set_editor_to_issue(self, editor, issue, newspaper):
        editor.assign_issue(issue, newspaper)
        issue.set_editor(editor)

    def get_any_other_editor_same_newspaper(self, editor: Editor, newspaper: Newspaper) -> Optional[Editor]:
        for other_editor in self.editors:
            if other_editor.editor_id != editor.editor_id and newspaper in other_editor.newspapers:
                return other_editor
        return None

    def get_editor_issues_ids(self, editor: Editor):
        return editor.get_editor_issues_ids()


    def get_issue(self, issue_id: Union[int,str]) -> Optional[Issue]:
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None

# Subscriber related methods
    def add_subscriber(self, new_subscriber: Subscriber):
        self.subscriber.append(new_subscriber)

    def all_subscribers(self) -> List[Subscriber]:
        return self.subscriber


    def get_subscriber(self, subscriber_id: Union[int,str]) -> Optional[Subscriber]:
        for subscriber in self.subscriber:
            if subscriber.subscriber_id == subscriber_id:
                return subscriber
        return None

    def remove_subscriber(self, subscriber: Subscriber):
        for subscriber in self.subscriber:
            if subscriber.subscriber_id == subscriber.subscriber_id:
                self.subscriber.remove(subscriber)