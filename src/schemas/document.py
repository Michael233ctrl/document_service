from pydantic import BaseModel, ConfigDict
from odmantic import ObjectId

from .user import User


class DocumentBase(BaseModel):
    title: str
    content: str


class DocumentCreate(DocumentBase):
    author: User | None = None


class DocumentUpdate(DocumentBase):
    ...


class DocumentInDBBase(DocumentBase):
    id: ObjectId | None = None
    model_config = ConfigDict(from_attributes=True)


class Document(DocumentInDBBase):
    author: User
