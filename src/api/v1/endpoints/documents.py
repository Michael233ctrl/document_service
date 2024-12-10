from typing import List, Any

from fastapi import APIRouter, Depends, Body, HTTPException
from motor.core import AgnosticDatabase
from odmantic import ObjectId

from src import schemas, crud, models
from src.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Document)
async def create_document(
        *,
        db: AgnosticDatabase = Depends(deps.get_db),
        title: str = Body(...),
        content: str = Body(...),
        current_user: models.User = Depends(deps.get_current_active_superuser),
):
    document_in = schemas.DocumentCreate(title=title, content=content, author=current_user)
    document =  await crud.document.create(db, obj_in=document_in)
    return document

@router.get("/", response_model=List[schemas.Document])
async def read_all_documents(
        *,
        db: AgnosticDatabase = Depends(deps.get_db),
        _: models.User = Depends(deps.get_current_active_superuser),
        page: int = 0,
) -> Any:
    """
    Retrieve all documents.
    """
    return await crud.document.get_multi(db=db, page=page)


@router.get("/{document_id}", response_model=schemas.Document)
async def read_document(
        *,
        db: AgnosticDatabase = Depends(deps.get_db),
        document_id: str,
        _: models.User = Depends(deps.get_current_active_user),
):
    document = await crud.document.get(db=db, id=document_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="The document is not available.",
        )

    return document


@router.put("/{document_id}", response_model=schemas.Document)
async def update_document(
        *,
        db: AgnosticDatabase = Depends(deps.get_db),
        document_id: ObjectId,
        obj_in: schemas.DocumentUpdate,
        _: models.User = Depends(deps.get_current_active_superuser),
):
    document = await crud.document.get(db=db, id=document_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="The document is not available.",
        )

    document_version_in = schemas.DocumentVersionCreate(
        document_id=document.id,
        title=document.title,
        content=document.content
    )
    """
    Enable Replica Set for transactions
    async with await db.client.start_session() as session:
        async with session.start_transaction():    
    """

    document_version = await crud.document_version.create(db, obj_in=document_version_in)
    document = await crud.document.update(
        db=db,
        db_obj=document,
        document_version_db_obj=document_version,
        obj_in=obj_in,
    )

    return document


@router.delete("/{document_id}", status_code=204)
async def delete_document(
        *,
        db: AgnosticDatabase = Depends(deps.get_db),
        document_id: ObjectId,
        _: models.User = Depends(deps.get_current_active_superuser),
):
    document = await crud.document.get(db=db, id=document_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="The document is not available.",
        )
    await crud.document.remove(db, db_obj=document)