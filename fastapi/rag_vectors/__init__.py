from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from langchain.retrievers import MultiQueryRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel

async def init_app(app):
    from prompt.const import PROMPT_TEMPLATE_2
    from .const import EMBED_MODEL, LLM_MODEL, LLM_STRUCT_MODEL
    from .controller import router
    from .retriever import PgRagRetriever

    app.include_router(router)

    class SpecAnswerEngine:
        def __init__(
            self, db_url: str, embed_model: str, llm_model: str, llm_struct_model: str, k: int = 20, distance: str = "cosine",
        ):
            # DB session
            self.engine_async = create_async_engine(db_url)
            self.SessionAsync = async_sessionmaker(self.engine_async, expire_on_commit=False)

            # Embeddings
            self.embeddings = OpenAIEmbeddings(model=embed_model)

            # Retriever
            self.cus_retriever = PgRagRetriever(
                embed_query=self.embeddings.embed_query, async_session_factory=self.SessionAsync, k=k, distance=distance,
            )

            # LLM
            self.llm = ChatOpenAI(model=llm_model, temperature=0)
            self.m_retriever = MultiQueryRetriever.from_llm(
                retriever=self.cus_retriever, llm=self.llm
            )

            # 結構化輸出的 LLM
            self.llm_struct_model = llm_struct_model

        async def answer_with_spec(self, question: str, output_format: BaseModel, max_ctx_chars: int = 3000) -> BaseModel:
            llm_struct = ChatOpenAI(model=self.llm_struct_model, temperature=0).with_structured_output(output_format)

            docs = await self.m_retriever.ainvoke(question)
            context = "\n\n".join((d.page_content or "").strip() for d in docs if d.page_content)[:max_ctx_chars]
            prompt = PROMPT_TEMPLATE_2.format(question, context)
            return await llm_struct.ainvoke(prompt)

    app.state.spec_answer_engine = SpecAnswerEngine(
        app.state.config['DATABASE_URL'],
        embed_model=EMBED_MODEL,
        llm_model=LLM_MODEL,
        llm_struct_model=LLM_STRUCT_MODEL,
    )