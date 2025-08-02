from fastapi_basic.base_factory import BaseFactory

from database import engine, Base
from version import version
from prompt import init_app as init_prompt_app

class AppFactory(BaseFactory):
    def get_app_config(self):
        from config import Config

        config = Config()
        return config.dict()

    def create_app(self):
        app = super().create_app()

        @app.on_event("startup")
        async def initail_app():
            await init_prompt_app(app)

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        @app.get("/hello")
        async def hello():
            return {
                'data': {
                    'version': version
                }
            }

        return app

app = AppFactory().create_app()