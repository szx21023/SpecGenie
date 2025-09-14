from select import select
from main import app

from typing import List, Optional
from sqlalchemy import select, literal
from sqlalchemy.ext.asyncio import AsyncSession
from .const import VECTOR_DIMENSION
from .model import RagVectors, Vector
from .schema import RagVectorSchema

class RagVectorService:
    @staticmethod
    async def create_rag_vector(db, data):
        schema = RagVectorSchema()
        data = schema.load(data)
        result = app.state.embedding_client.embed_one(str(data))
        data['embedding'] = result # f"[{', '.join(str(x) for x in result)}]" if isinstance(result, list) else result

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
        vector_query = await RagVectorService.convert_data_to_vector(db, prompt)
        result = await RagVectorService.search_vectors_orm(db, qvec=vector_query, k=12)
        return result

    @staticmethod
    async def convert_data_to_vector(db, data):
        result = app.state.embedding_client.embed_one(str(data))
        return f"[{', '.join(str(x) for x in result)}]" if isinstance(result, list) else result

    @staticmethod
    async def search_vectors_orm(
        db: AsyncSession,
        *,
        qvec: list[float],                # 你已經用 embedding API 轉好的查詢向量
        k: int = 12,
        mode: Optional[str] = None,
        role: Optional[str] = None,
        source_type: Optional[str] = None,
    ) -> List[dict]:
        # 把 qvec 綁成 ORM 可以理解的「public.vector(維度)」常值
        qlit = literal(qvec, type_=Vector(VECTOR_DIMENSION))

        # 定義「距離」與「相似度」表達式
        dist_expr = RagVectors.embedding.op('<=>')(qlit)             # cosine 距離（越小越近）
        sim_expr  = (1 - dist_expr).label('similarity')              # 轉成相似度（越大越好，可選）

        stmt = (
            select(
                *[col for col in RagVectors.__table__.columns if col.name != 'embedding'],  # 不選 embedding 欄位
                sim_expr,
            )
            # 過濾條件（依需要加）
            .where(*(cond for cond in [
                (RagVectors.mode == mode) if mode else None,
                (RagVectors.role == role) if role else None,
                (RagVectors.source_type == source_type) if source_type else None,
            ] if cond is not None))
            # 依距離排序（最相近在前）
            .order_by(dist_expr)
            .limit(k)
        )

        rows = (await db.execute(stmt)).mappings().all()
        return [dict(r) for r in rows]

