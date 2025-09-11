from main import app
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(app.state.config.get("DATABASE_URL"), echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# 依賴注入
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    # 在這裡可以添加一些共用的欄位或方法

    create_time: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now(), onupdate=func.now())