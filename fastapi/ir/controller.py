from database import get_db

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import IRService

router = APIRouter(prefix=f"/ir", tags=["ir"])

@router.get("")
async def get_ir(
        db: AsyncSession = Depends(get_db)
    ):
    """
    get ir api
    """

    result = await IRService.get_ir(db)
    return result