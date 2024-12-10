from typing import Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from motor.core import AgnosticDatabase
from odmantic.engine import AIOSessionType

from src.crud.base import CRUDBase, ModelType, UpdateSchemaType, CreateSchemaType
from src.models.document_version import DocumentVersion
from src.models.document import Document
from src.schemas import DocumentCreate, DocumentUpdate
from src.utils.common import datetime_now_sec


class CRUDDocument(CRUDBase[Document, DocumentCreate, DocumentUpdate]):
    async def update(  # noqa
            self,
            db: AgnosticDatabase,
            *,
            db_obj: Document,
            document_version_db_obj: DocumentVersion,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
            session: AIOSessionType = None
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        # TODO: Check if this saves changes with the setattr calls
        db_obj.modified = datetime_now_sec()
        db_obj.versions.append(document_version_db_obj.id)

        await self.engine.save(db_obj, session=session)
        return db_obj


document = CRUDDocument(Document)
