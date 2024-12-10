from odmantic import ObjectId
from pydantic import BaseModel


class DocumentVersionBase(BaseModel):
    document_id: ObjectId
    title: str
    content: str
    version: int | None = None


class DocumentVersionCreate(DocumentVersionBase):
    ...

class DocumentVersionUpdate(DocumentVersionBase):
    ...