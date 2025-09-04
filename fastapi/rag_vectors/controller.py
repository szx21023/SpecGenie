from database import get_db

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import RagVectorService

router = APIRouter(prefix=f"/rag_vectors", tags=["rag_vectors"])

@router.post("")
async def post_rag_vectors(
        schema = Body(example={
            'prompt': 'Sample Prompt'
        }),
        db: AsyncSession = Depends(get_db)
    ):

    prompt = schema.get('prompt')
    result = await RagVectorService.get_rag_vector_by_prompt(db, prompt)
    return result