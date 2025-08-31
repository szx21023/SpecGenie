from main import app
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(app.state.config.get("DATABASE_URL"), echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# 依賴注入
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

from sqlalchemy.orm import declarative_base
Base = declarative_base()