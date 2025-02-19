from typing import List

from fastapi.encoders import jsonable_encoder
from motor.core import AgnosticDatabase
from odmantic import ObjectId
from odmantic.engine import AIOSessionType

from src.crud.base import CRUDBase
from src.models.document import Document
from src.models.document_version import DocumentVersion
from src.schemas import DocumentVersionCreate, DocumentVersionUpdate
from src.core.config import settings
from src.utils.common import datetime_now_sec


class CRUDDocumentVersion(
    CRUDBase[DocumentVersion, DocumentVersionCreate, DocumentVersionUpdate]
):
    async def get_by_document_id(
        self, db: AgnosticDatabase, document_id: ObjectId
    ) -> List[DocumentVersion]:
        return await self.engine.find(
            DocumentVersion,
            DocumentVersion.document_id == document_id,
            sort=(DocumentVersion.version.desc()),
        )

    async def create(  # noqa
        self,
        db: AgnosticDatabase,
        *,
        obj_in: DocumentVersionCreate,
        session: AIOSessionType = None,
    ) -> DocumentVersion:
        document_history_amount = await self.engine.count(
            DocumentVersion,
            DocumentVersion.document_id == obj_in.document_id,
        )
        if document_history_amount >= settings.LIMIT_OF_DOCUMENT_VERSIONS:
            oldest_version = await self.engine.find_one(
                DocumentVersion,
                DocumentVersion.document_id == obj_in.document_id,
                sort=(DocumentVersion.created.asc()),
            )
            if oldest_version:
                await self.engine.delete(oldest_version)

        latest_doc_version = await self.engine.find_one(
            DocumentVersion,
            DocumentVersion.document_id == obj_in.document_id,
            sort=(DocumentVersion.created.desc()),
        )
        if latest_doc_version:
            obj_in.version = latest_doc_version.version + 1

        obj_in_data = jsonable_encoder(obj_in, exclude_none=True)
        db_obj = self.model(**obj_in_data)  # type: ignore
        return await self.engine.save(db_obj, session=session)

    async def rollback(
        self,
        db: AgnosticDatabase,
        *,
        document_version_db_obj: DocumentVersion,
    ) -> None:
        latest_doc_version = await self.engine.find_one(
            DocumentVersion,
            DocumentVersion.document_id == document_version_db_obj.document_id,
            sort=(DocumentVersion.created.desc()),
        )
        if latest_doc_version:
            document_version_db_obj.version = latest_doc_version.version + 1

        document_version_db_obj.created = datetime_now_sec()
        await self.engine.save(document_version_db_obj)


document_version = CRUDDocumentVersion(DocumentVersion)
