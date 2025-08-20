from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Apis(Base):
    __tablename__ = "apis"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    method: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    request_fields: Mapped[list] = mapped_column(JSON, nullable=False)
    response_fields: Mapped[list] = mapped_column(JSON, nullable=False)
