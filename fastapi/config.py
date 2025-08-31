from fastapi_basic.base_config import BaseConfig

class Config(BaseConfig):
    OPENAI_API_KEY: str = ""
    LOGGER_NAME: str|None = 'test'

    DATABASE_URL : str = "sqlite+aiosqlite:///./test.db" # 非同步 SQLite URI：注意是 sqlite+aiosqlite