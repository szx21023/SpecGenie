from sqlalchemy.orm import Mapped, mapped_column

from database import BaseModel

class DocsPost(BaseModel):
    __tablename__ = "docs_posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
