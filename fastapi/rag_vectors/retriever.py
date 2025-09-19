# retrievers/pg_rag_retriever.py
from typing import Any, Callable, Dict, List, Optional, Literal
from sqlalchemy import select
from sqlalchemy.orm import Session as SyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document

from rag_vectors.model import RagVectors  # ← 改成你的實際路徑


class PgRagRetriever(BaseRetriever):
    # === 把屬性宣告成 Pydantic 欄位 ===
    embed_query: Callable[[str], List[float]]
    async_session_factory: Optional[Callable[[], AsyncSession]] = None
    sync_session_factory: Optional[Callable[[], SyncSession]] = None
    k: int = 5
    distance: Literal["cosine", "l2"] = "cosine"
    filters: Optional[Dict[str, Any]] = None

    class Config:
        arbitrary_types_allowed = True  # 允許 Callable、Session 這些非內建型別

    # ---- sync 路徑（BaseRetriever 要求）----
    def _get_relevant_documents(self, query: str) -> List[Document]:
        if self.sync_session_factory is None:
            # 沒 sync session，就用 async 路徑（阻塞式執行）
            import asyncio
            return asyncio.run(self._aget_relevant_documents(query))

        qvec = self.embed_query(query)
        with self.sync_session_factory() as session:
            stmt = select(RagVectors).where(RagVectors.embedding.is_not(None))
            if self.filters:
                st = self.filters.get("source_type")
                if st is not None:
                    stmt = stmt.where(RagVectors.source_type == st)
                sid = self.filters.get("source_id")
                if sid is not None:
                    stmt = stmt.where(RagVectors.source_id == sid)

            if self.distance == "cosine":
                stmt = stmt.order_by(RagVectors.embedding.cosine_distance(qvec))
            else:
                stmt = stmt.order_by(RagVectors.embedding.l2_distance(qvec))
            rows = session.execute(stmt.limit(self.k)).scalars().all()

        return [
            Document(
                page_content=r.text or "",
                metadata={
                    "id": r.id,
                    "source_type": r.source_type,
                    "source_id": r.source_id,
                    "mode": r.mode,
                    "role": r.role,
                },
            )
            for r in rows
        ]

    # ---- async 路徑（FastAPI 推薦用這個）----
    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        if self.async_session_factory is None:
            import asyncio
            return await asyncio.to_thread(self._get_relevant_documents, query)

        import asyncio as _asyncio
        qvec = await _asyncio.to_thread(self.embed_query, query)

        async with self.async_session_factory() as session:
            # 1) 先組距離表達式
            if self.distance == "cosine":
                dist_col = RagVectors.embedding.cosine_distance(qvec)
            else:
                dist_col = RagVectors.embedding.l2_distance(qvec)

            # 2) 在 SELECT 中同時選 RagVectors + 距離欄位
            stmt = (
                select(RagVectors, dist_col.label("distance"))
                .where(RagVectors.embedding.is_not(None))
            )

            # 可選的 filters
            if self.filters:
                st = self.filters.get("source_type")
                if st is not None:
                    stmt = stmt.where(RagVectors.source_type == st)
                sid = self.filters.get("source_id")
                if sid is not None:
                    stmt = stmt.where(RagVectors.source_id == sid)

            # 3) 依距離排序 + 限制數量
            stmt = stmt.order_by(dist_col).limit(self.k)

            # 4) 不能用 .scalars()，要拿 (RagVectors, distance) tuples
            rows = (await session.execute(stmt)).all()

        return [
            Document(
                page_content=r.text or "",
                metadata={
                    "id": r.id,
                    "source_type": r.source_type,
                    "source_id": r.source_id,
                    "mode": r.mode,
                    "role": r.role,
                    "distance": float(distance),
                    "similarity": 1.0 - float(distance) if self.distance == "cosine" else 1.0 / (1.0 + float(distance)),
                },
            )
            for r, distance in rows
        ]
