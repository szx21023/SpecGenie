from main import app
from sqlalchemy import desc, select

from outlines import from_openai
from pydantic import BaseModel

from ir.schema import IR
from ir.service import IRService
from apis.service import ApisService
from rag_vectors.const import VectorSourceType
from rag_vectors.service import RagVectorService
from tables.service import TablesService

from .const import Ops, IrTypes, PROMPT_TEMPLATE, ModeTypes, RoleTypes
from .model import Prompts
from .schema import PromptSchema, Plan, Advice

class PromptService:
    @staticmethod
    async def set_q_order():
        orders = [desc(Prompts.id)]

        return orders

    @staticmethod
    async def prompt(db, prompt: str, output_format: BaseModel, model_name: str = "gpt-4o"):
        """
        Create a new prompt with the given prompt.
        """
        # Create the model
        app.logger.info(f'Using model: {model_name}, prompt: {prompt}')
        model = from_openai(
            app.state.openai_client,
            model_name
        )

        result = model(
            prompt,
            output_format
        )

        answer = output_format.model_validate_json(result)
        return answer.model_dump()

    @staticmethod
    async def create_prompt(db, prompt: str, mode: str, role: str):
        """
        Test the prompt with the given ID.
        """

        schema = PromptSchema()
        data = schema.load({"prompt": prompt, "mode": mode, "role": role})

        prompt = Prompts(**data)
        db.add(prompt)
        try:
            await db.commit()
            await db.refresh(prompt)

        except Exception as e:
            await db.rollback()
            raise e

        return prompt

    @staticmethod
    async def get_prompts(db):
        q_order = await PromptService.set_q_order()

        sql = select(Prompts).order_by(*q_order)
        result = await db.execute(sql)
        prompts = result.scalars().all()

        schema = PromptSchema(many=True)
        prompts = schema.dump(prompts)
        return prompts

    @staticmethod
    async def prompt_to_model(db, user_prompt: str, mode: str):
        if mode == ModeTypes.SPEC:
            result = await PromptService.prompt_to_spec_model(db, user_prompt)

        elif mode == ModeTypes.ADVICE:
            result = await PromptService.prompt_to_advice_model(db, user_prompt)

        prompt = await PromptService.create_prompt(db, user_prompt, mode, RoleTypes.USER)
        data = {
            'source_type': VectorSourceType.PROMPT,
            'source_id': str(prompt.id),
            'mode': mode,
            'role': RoleTypes.USER,
            'text': user_prompt
        }
        _ = await RagVectorService.create_rag_vector(db, data)
        prompt = await PromptService.create_prompt(db, str(result), mode, RoleTypes.SYSTEM)
        data = {
            'source_type': VectorSourceType.PROMPT,
            'source_id': str(prompt.id),
            'mode': mode,
            'role': RoleTypes.SYSTEM,
            'text': str(result)
        }
        _ = await RagVectorService.create_rag_vector(db, data)
        return result

    @staticmethod
    async def prompt_to_spec_model(db, user_prompt: str):
        irs = await IRService.get_ir(db)
        app.logger.info(f'irs: {irs}')
        prompt = PROMPT_TEMPLATE.format(user_prompt, str(irs))

        answer = await PromptService.prompt(db, prompt, Plan)
        app.logger.info(answer)
        for operator in answer.get('operations'):
            ops = operator.get('kind')
            by, value = operator.get('target', {}).get('by'), operator.get('target', {}).get('value')
            if ops == Ops.ADD_TABLE:
                data = {
                    'name': operator.get('name'),
                    'columns': operator.get('columns', [])
                }
                await TablesService.create_table(db, data)

            elif ops == Ops.UPDATE_TABLE:
                current_table = await PromptService.get_current_spec(irs, IrTypes.ENTITY, by, value)
                data = {
                    'columns': operator.get('final_columns', [])
                }
                await TablesService.update_table(db, int(current_table.get('id')), data)

            elif ops == Ops.DROP_TABLE:
                current_table = await PromptService.get_current_spec(irs, IrTypes.ENTITY, by, value)
                await TablesService.delete_table(db, int(current_table.get('id')))

            elif ops == Ops.ADD_API:
                data = {
                    'method': operator.get('method'),
                    'path': operator.get('path'),
                    'request_fields': operator.get('request_fields', []),
                    'response_fields': operator.get('response_fields', [])
                }
                await ApisService.create_api(db, data)

            elif ops == Ops.UPDATE_API:
                current_api = await PromptService.get_current_spec(irs, IrTypes.API, by, value)
                data = {
                    'method': operator.get('method', current_api.get('method')),
                    'path': operator.get('path', current_api.get('path')),
                    'request_fields': operator.get('final_request_fields', []),
                    'response_fields': operator.get('final_response_fields', [])
                }
                await ApisService.update_api(db, int(current_api.get('id')), data)

            elif ops == Ops.DROP_API:
                current_api = await PromptService.get_current_spec(irs, IrTypes.API, by, value)
                await ApisService.delete_api(db, int(current_api.get('id')))

            else:
                pass

        return answer

    @staticmethod
    async def prompt_to_advice_model(db, user_prompt: str):
        irs = await IRService.get_ir(db)
        app.logger.info(f'irs: {irs}')
        prompt = PROMPT_TEMPLATE.format(user_prompt, str(irs))
        answer = await PromptService.prompt(db, prompt, Advice)

        return answer

    @staticmethod
    async def get_current_spec(irs, type, by, value):
        if type == IrTypes.ENTITY:
            entities = irs.get('entities', [])
            for entity in entities:
                if str(entity.get(by)) != str(value):
                    continue

                return entity

        elif type == IrTypes.API:
            apis = irs.get('apis', [])
            for api in apis:
                if str(api.get(by)) != str(value):
                    continue

                return api

   # fastapi/prompt/service.py
    @staticmethod
    async def langchain_test():
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from langchain_openai import OpenAIEmbeddings
        from rag_vectors.retriever import PgRagRetriever

        engine_async = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/pgvector_demo")
        SessionAsync = async_sessionmaker(engine_async, expire_on_commit=False)

        emb = OpenAIEmbeddings(model="text-embedding-3-small")
        retr = PgRagRetriever(
            embed_query=emb.embed_query,
            async_session_factory=SessionAsync,
            k=20,
            distance="cosine",
        )

        docs = await retr.ainvoke("tell me about dogs")
        print(docs)
        for d in docs:
            print(d.page_content, d.metadata)
            print('-------')


        # from sqlalchemy import create_engine
        # from sqlalchemy.orm import sessionmaker
        # from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        # from langchain_openai import OpenAIEmbeddings
        from langchain.retrievers import MultiQueryRetriever
        from langchain_openai import ChatOpenAI
        # from rag_vectors.retriever import PgRagRetriever

        # # 建議：app 用 async engine；sync 用於某些同步鏈條相容
        # async_engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/pgvector_demo")
        # SessionAsync = async_sessionmaker(async_engine, expire_on_commit=False)

        # sync_engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/pgvector_demo")
        # SessionSync = sessionmaker(sync_engine)

        # emb = OpenAIEmbeddings(model="text-embedding-3-small")

        # retr = PgRagRetriever(
        #     embed_query=emb.embed_query,
        #     async_session_factory=SessionAsync,
        #     sync_session_factory=SessionSync,
        #     k=5,
        #     distance="cosine",
        # )

        # # 直接用（同步）
        # docs = retr.invoke("dogs")  # 會走 sync session
        # # 或在 FastAPI 協程裡（非阻塞）
        # docs = await retr.ainvoke("dogs")

        # # 接 MultiQuery（若你用 async 環境，建議也用 ainvoke）
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        mqr = MultiQueryRetriever.from_llm(retriever=retr, llm=llm)
        # docs = mqr.invoke("best loyal pets")        # 同步
        # # 或：
        docs = await mqr.ainvoke("best loyal pets") # 非同步
        print('aaaaaaaaaaaaaaaaaaa')
        print(docs)
        for d in docs:
            print(d.page_content, d.metadata)
            print('-------')
