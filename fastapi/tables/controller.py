from database import get_db

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .const import CREATE_TABLE_EXAMPLE
from .service import TablesService

router = APIRouter(prefix=f"/tables", tags=["tables"])

@router.get("")
async def get_tables(
        db: AsyncSession = Depends(get_db)
    ):
    """
    get tables api
    """

    result = await TablesService.get_tables(db)
    return result

@router.post("")
async def create_table(
        schema = Body(example=CREATE_TABLE_EXAMPLE), db: AsyncSession = Depends(get_db)
    ):
    """
    create table api
    """

    result = await TablesService.create_table(db, schema)
    return result