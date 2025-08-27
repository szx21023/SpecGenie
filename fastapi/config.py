from fastapi_basic.base_config import BaseConfig

class Config(BaseConfig):
    OPENAI_API_KEY: str = ""
    LOGGER_NAME: str|None = 'test'