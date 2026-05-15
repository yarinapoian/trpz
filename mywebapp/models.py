from datetime import datetime


class Task:
    def __init__(self, id: int = None, title: str = None, status: str = "todo", created_at: datetime = None):
        self.id = id
        self.title = title
        self.status = status
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }

    def to_dict_compact(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
