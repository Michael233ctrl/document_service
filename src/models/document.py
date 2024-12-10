from datetime import datetime
from odmantic import Field, Reference, ObjectId

from src.db.base_class import Base
from src.utils.common import datetime_now_sec

from .user import User


class Document(Base):
    created: datetime = Field(default_factory=datetime_now_sec)
    modified: datetime = Field(default_factory=datetime_now_sec)
    title: str = Field(default="")
    content: str = Field(default="")
    author: User = Reference()
    versions: list[ObjectId] = Field(default_factory=list)
