from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector  # ← 重點

from database import BaseModel

from .const import VECTOR_DIMENSION

class RagVectors(BaseModel):
    __tablename__ = "rag_vectors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 來源
    source_type: Mapped[str] = mapped_column(nullable=True)
    source_id: Mapped[str] = mapped_column(nullable=True)
    mode: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=True)
    # 內文
    text: Mapped[str] = mapped_column(nullable=True)
    # Example for PostgreSQL with pgvector extension
    embedding: Mapped[list[float]] = mapped_column(Vector(VECTOR_DIMENSION), nullable=True)
