from typing import List
from fastapi_basic.base_factory import BaseFactory

from version import version
from ext.openai import init_app as init_openai_app
from apis import init_app as init_apis_app
from docs_posts import init_app as init_docs_posts_app
from ir import init_app as init_ir_app
from prompt import init_app as init_prompt_app
from rag_vectors import init_app as init_rag_vectors_app
from tables import init_app as init_tables_app

class AppFactory(BaseFactory):
    def get_app_config(self):
        from config import Config
        config = Config()
        return config.dict()

    async def __setup_llm_client(self, app):
        class EmbeddingClient:
            """
            傳入你現有的 openai client（如 app.state.openai_client）
            """
            def __init__(self, client, model: str = "text-embedding-3-small"):
                self.client = client
                self.model = model

            def embed_one(self, text: str) -> List[float]:
                resp = self.client.embeddings.create(
                    model=self.model,
                    input=[text]
                )
                return resp.data[0].embedding

            def embed_batch(self, texts: List[str]) -> List[List[float]]:
                resp = self.client.embeddings.create(
                    model=self.model,
                    input=texts
                )
                return [d.embedding for d in resp.data]

        app.state.openai_client = await init_openai_app(app)
        app.state.embedding_client = EmbeddingClient(app.state.openai_client)

    def create_app(self):
        app = super().create_app()

        @app.on_event("startup")
        async def initail_app():
            await init_apis_app(app)
            await init_docs_posts_app(app)
            await init_ir_app(app)
            await init_prompt_app(app)
            await init_rag_vectors_app(app)
            await init_tables_app(app)

            await self.__setup_llm_client(app)

            # ✅ 先建立 pgvector extension，再 create_all
            from sqlalchemy import text
            from database import engine, Base
            async with engine.begin() as conn:
                # 印出連到哪個 DB，避免誤連錯庫
                dbname = (await conn.execute(text("SELECT current_database()"))).scalar_one()
                print(f"[DB] connected to: {dbname}")

                # 安裝/確保 pgvector 存在（同一 DB 跑多次也不會出錯）
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

                # （可選）保險：設定 search_path
                await conn.execute(text("SET search_path TO public, pg_catalog"))

                # 最後才建表
                await conn.run_sync(Base.metadata.create_all)

        @app.get("/hello")
        async def hello():
            return {"data": {"version": version}}

        return app

app = AppFactory().create_app()
