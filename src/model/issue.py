class Issue(object):
    def __init__(self, releasedate,  page: int , editor: int , issue_id: int, released: bool = False,):
        self.release_date = releasedate
        self.released: bool = released
        self.page : int = page
        self.editor_id : int = editor
        self.issue_id : int = issue_id
        self.subscribers = []

    def set_editor(self, editor):
        self.editor_id = editor

    def get_issue_by_id(self, issue_id):
        return self.issue_id

    def deliver_issue_id_to_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
        subscriber.delivered_issues.append(self)

    def serialize(self):
        return {
            "issue_id": self.issue_id,
            "release_date": self.release_date,
            "pages": self.page,
            "editor": self.editor_id,
            "released": self.released,
            "subscribers": [subscriber.subscriber_id for subscriber in self.subscribers]
        }