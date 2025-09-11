from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import BaseModel

class Prompts(BaseModel):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    prompt: Mapped[str] = mapped_column()
    mode: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
