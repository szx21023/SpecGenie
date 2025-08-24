from database import get_db

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import PromptService

router = APIRouter(prefix=f"/prompt", tags=["prompt"])

@router.get("")
async def get_prompts(
        db: AsyncSession = Depends(get_db)
    ):
    """
    get prompts api
    """

    result = await PromptService.get_prompts(db)
    return result

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
    result = await PromptService.prompt_to_model(db, prompt=prompt)
    return result

@router.post("/test")
async def create_test_data( 
        schema = Body(example={
            'prompt': 'Sample Prompt',
        }),
        db: AsyncSession = Depends(get_db)
    ):
    """
    post test data api
    """

    prompt = schema.get('prompt')
    result = await PromptService.create_test_prompt(db, prompt=prompt)
    return result