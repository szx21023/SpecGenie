from database import get_db

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import PromptService

router = APIRouter(prefix=f"/prompt", tags=["prompt"])

@router.post("")
async def create_prompt( 
        schema = Body(example={
            'prompt': 'Sample Prompt',
        }),
        db: AsyncSession = Depends(get_db)
    ):
    """
    post prompt api
    """

    prompt = schema.get('prompt')
    result = await PromptService.create_prompt(db, prompt=prompt)
    return result