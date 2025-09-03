from select import select
from main import app
from .model import RagVectors
from .schema import RagVectorSchema

class RagVectorService:
    @staticmethod
    async def create_rag_vector(db, data):
        schema = RagVectorSchema()
        data = schema.load(data)
        result = app.state.embedding_client.embed_one(str(data))
        data['embedding'] = f"[{', '.join(str(x) for x in result)}]" if isinstance(result, list) else result

        rag_vector = RagVectors(**data)
        db.add(rag_vector)
        try:
            await db.commit()
            await db.refresh(rag_vector)

        except Exception as e:
            await db.rollback()
            raise e

        return rag_vector
    
    @staticmethod
    async def get_rag_vector_by_prompt(db, prompt):
        vector_query = RagVectorService.convert_data_to_vector(db, prompt)
        result = await db.execute(
            select(RagVectors).where(RagVectors.prompt == prompt)
        )
        return result.scalars().first()
    
    @staticmethod
    async def convert_data_to_vector(db, data):
        result = app.state.embedding_client.embed_one(str(data))
        return f"[{', '.join(str(x) for x in result)}]" if isinstance(result, list) else result
