from main import app
from sqlalchemy import select

from .schema import ApisSchema
from .model import Apis

class ApisService:
    @staticmethod
    async def create_api(db, api, **kwargs):
        schema = ApisSchema()
        data = schema.load(api)

        api = Apis(**data)
        db.add(api)
        try:
            await db.commit()
            await db.refresh(api)

        except Exception as e:
            await db.rollback()
            raise e

        return api

    @staticmethod
    async def get_apis(db):
        sql = select(Apis)
        result = await db.execute(sql)
        apis = result.scalars().all()

        schema = ApisSchema(many=True)
        apis = schema.dump(apis)
        return apis
