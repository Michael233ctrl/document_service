from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from motor.core import AgnosticDatabase
from odmantic import ObjectId

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Document)
async def create_document(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    title: str = Body(...),
    content: str = Body(...),
    current_user: models.User = Depends(deps.get_current_user),
):
    document = await crud.document.create(
        db,
        obj_in=schemas.DocumentCreate(
            title=title, content=content, author=current_user
        ),
    )
    await crud.document_version.create(
        db,
        obj_in=schemas.DocumentVersionCreate(
            document_id=document.id, title=document.title, content=document.content
        ),
    )
    return document


@router.get("/", response_model=List[schemas.Document])
async def read_all_documents(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    _: models.User = Depends(deps.get_current_user),
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
    document_id: ObjectId,
    _: models.User = Depends(deps.get_current_user),
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
    _: models.User = Depends(deps.get_current_user),
):
    document = await crud.document.get(db=db, id=document_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="The document is not available.",
        )
    if document.title == obj_in.title and document.content == obj_in.content:
        raise HTTPException(
            status_code=204,
            detail="The document data is not changed.",
        )

    document_version_in = schemas.DocumentVersionCreate(
        document_id=document.id, title=obj_in.title, content=obj_in.content
    )

    """
    The 'update_document' function has a potential issue with data inconsistency.
    The issue raised if document update fails.

    TODO: turn on the transactions and put the create/update DB operations 
    into a context manager to resolve the issue.

    Example:
    async with await db.client.start_session() as session:
        async with session.start_transaction():    
    """
    await crud.document_version.create(db, obj_in=document_version_in)
    document = await crud.document.update(
        db=db,
        document_db_obj=document,
        obj_in=obj_in,
    )

    return document


@router.delete("/{document_id}", status_code=204)
async def delete_document(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    document_id: ObjectId,
    _: models.User = Depends(deps.get_current_user),
):
    document = await crud.document.get(db=db, id=document_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="The document is not available.",
        )
    await crud.document.remove(db, db_obj=document)


@router.get("/{document_id}/history")
async def read_document_version_history(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    document_id: ObjectId,
    _: models.User = Depends(deps.get_current_user),
):
    versions = await crud.document_version.get_by_document_id(db, document_id)
    return versions


@router.post("/{document_id}/{document_version_id}/rollback")
async def rollback_document(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    document_id: ObjectId,
    document_version_id: ObjectId,
    _: models.User = Depends(deps.get_current_user),
):
    document = await crud.document.get(db=db, id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="The document is not available.")

    document_version = await crud.document_version.get(db=db, id=document_version_id)
    if not document_version:
        raise HTTPException(
            status_code=404, detail="The document version is not available."
        )

    """    
    TODO: turn on the transaction in case data inconsistency.

    Example:
    async with await db.client.start_session() as session:
        async with session.start_transaction():
    """
    await crud.document.rollback(
        db, document_db_obj=document, document_version_db_obj=document_version
    )
    await crud.document_version.rollback(db, document_version_db_obj=document_version)

    return document
