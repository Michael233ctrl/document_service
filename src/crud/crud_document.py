from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from motor.core import AgnosticDatabase
from odmantic.engine import AIOSessionType

from src.crud.base import CRUDBase, UpdateSchemaType
from src.models.document import Document
from src.models.document_version import DocumentVersion
from src.schemas import DocumentCreate, DocumentUpdate
from src.utils.common import datetime_now_sec


class CRUDDocument(CRUDBase[Document, DocumentCreate, DocumentUpdate]):
    async def update(  # noqa
        self,
        db: AgnosticDatabase,
        *,
        document_db_obj: Document,
        document_version_db_obj: DocumentVersion,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        session: AIOSessionType = None
    ) -> Document:
        obj_data = jsonable_encoder(document_db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(document_db_obj, field, update_data[field])

        # TODO: Check if this saves changes with the setattr calls
        document_db_obj.modified = datetime_now_sec()
        await self.add_version(
            db,
            document_db_obj=document_db_obj,
            document_version_db_obj=document_version_db_obj,
            session=session,
        )
        await self.engine.save(document_db_obj, session=session)
        return document_db_obj

    async def rollback(
        self,
        db: AgnosticDatabase,
        *,
        document_db_obj: Document,
        document_version_db_obj: DocumentVersion,
        session: AIOSessionType = None
    ) -> Document:
        document_db_obj.title = document_version_db_obj.title
        document_db_obj.content = document_version_db_obj.content
        document_db_obj.modified = datetime_now_sec()
        await self.engine.save(document_db_obj, session=session)
        return document_db_obj

    async def add_version(
        self,
        db: AgnosticDatabase,
        *,
        document_db_obj: Document,
        document_version_db_obj: DocumentVersion,
        session: AIOSessionType = None
    ) -> Document:
        document_db_obj.versions.append(document_version_db_obj.id)
        await self.engine.save(document_db_obj, session=session)
        return document_db_obj


document = CRUDDocument(Document)
