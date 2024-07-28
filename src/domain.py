from dataclasses import dataclass
import datetime

@dataclass
class Post:
    id: str
    author: str
    title: str
    description: str
    votes: int
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    