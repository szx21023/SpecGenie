from main import app

from .model import RagVectors
from .schema import RagVectorSchema

class RagVectorService:
    @staticmethod
    async def create_rag_vector(db, data):
        schema = RagVectorSchema()
        data = schema.load(data)
        result = app.state.embedding_client.embed_one(str(data))
        data['embedding'] = result

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
    async def get_rag_vector_by_prompt(db, prompt, k):
        result = await app.state.spec_answer_engine.cus_retriever.ainvoke(prompt, k=k)
        return result
