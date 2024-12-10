from fastapi.encoders import jsonable_encoder
from motor.core import AgnosticDatabase
from odmantic.engine import AIOSessionType

from src.crud.base import CRUDBase, CreateSchemaType, ModelType
from src.models.document_version import DocumentVersion
from src.schemas import DocumentVersionCreate, DocumentVersionUpdate


class CRUDDocumentVersion(CRUDBase[DocumentVersion, DocumentVersionCreate, DocumentVersionUpdate]):
    async def create(  # noqa
            self,
            db: AgnosticDatabase,
            *,
            obj_in: CreateSchemaType,
            session: AIOSessionType = None,
    ) -> ModelType:
        version_number = await self.engine.count(
            DocumentVersion,
            DocumentVersion.document_id == obj_in.document_id,
        )
        if version_number >= 5:
            oldest_version = await self.engine.find_one(
                DocumentVersion,
                DocumentVersion.document_id == obj_in.document_id,
                sort=(DocumentVersion.created.asc())
            )
            await self.engine.delete(oldest_version)

        latest_doc_version = await self.engine.find_one(
            DocumentVersion,
            DocumentVersion.document_id == obj_in.document_id,
            sort=(DocumentVersion.created.desc())
        )
        if latest_doc_version:
            obj_in.version = latest_doc_version.version + 1

        obj_in_data = jsonable_encoder(obj_in, exclude_none=True)
        db_obj = self.model(**obj_in_data)  # type: ignore
        return await self.engine.save(db_obj, session=session)


document_version = CRUDDocumentVersion(DocumentVersion)
