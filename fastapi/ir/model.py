from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class IR(Base):
    __tablename__ = "ir"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entities: Mapped[list] = mapped_column(JSON, nullable=False)
    apis: Mapped[list] = mapped_column(JSON, nullable=False)