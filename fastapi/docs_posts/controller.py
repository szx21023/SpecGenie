from database import get_db

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .const import CREATE_DOCS_POST_EXAMPLE
from .service import DocsPostService

router = APIRouter(prefix=f"/docs_posts", tags=["docs_posts"])

@router.get("")
async def get_docs_posts(
        db: AsyncSession = Depends(get_db)
    ):
    """
    get docs posts api
    """

    result = await DocsPostService.get_docs_posts(db)
    return result

@router.post("")
async def create_post(
        schema = Body(example=CREATE_DOCS_POST_EXAMPLE), db: AsyncSession = Depends(get_db)
    ):
    """
    create post api
    """

    result = await DocsPostService.create_docs_post(db, schema)
    return result

@router.patch("/{post_id}")
async def update_post(
        post_id: int, schema = Body(example=CREATE_DOCS_POST_EXAMPLE), db: AsyncSession = Depends(get_db)
    ):
    """
    update post api
    """

    result = await DocsPostService.update_docs_post(db, post_id, schema)
    return result

@router.delete("/{post_id}")
async def delete_post(
        post_id: int, db: AsyncSession = Depends(get_db)
    ):
    """
    delete post api
    """

    result = await DocsPostService.delete_docs_post(db, post_id)
    return result