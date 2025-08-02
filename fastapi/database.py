from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# 非同步 SQLite URI：注意是 sqlite+aiosqlite
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

# 依賴注入
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session