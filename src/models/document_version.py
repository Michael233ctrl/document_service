from datetime import datetime
from odmantic import Field, ObjectId

from src.db.base_class import Base
from src.utils.common import datetime_now_sec


class DocumentVersion(Base):
    document_id: ObjectId
    version: int = Field(default=1)
    title: str = Field()
    content: str = Field()
    created: datetime = Field(default_factory=datetime_now_sec)