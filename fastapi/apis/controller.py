from database import get_db

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .const import CREATE_API_EXAMPLE
from .service import ApisService

router = APIRouter(prefix=f"/apis", tags=["apis"])

@router.get("")
async def get_apis(
        db: AsyncSession = Depends(get_db)
    ):
    """
    get apis
    """

    result = await ApisService.get_apis(db)
    return result

@router.post("")
async def create_api(
        schema = Body(example=CREATE_API_EXAMPLE), db: AsyncSession = Depends(get_db)
    ):
    """
    create api
    """

    result = await ApisService.create_api(db, schema)
    return result

@router.patch("/{api_id}")
async def update_api(
        api_id: int,
        schema = Body(example=CREATE_API_EXAMPLE),
        db: AsyncSession = Depends(get_db)
    ):
    """
    update api
    """

    result = await ApisService.update_api(db, api_id, schema)
    return result