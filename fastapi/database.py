from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

# 非同步 SQLite URI：注意是 sqlite+aiosqlite
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

# 依賴注入
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

class BaseModel(Base):
    __abstract__ = True  # 這個類不會在數據庫中創建表格

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    created_time: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
