from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Tables(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    columns: Mapped[list] = mapped_column(JSON, nullable=False)
