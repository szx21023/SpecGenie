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

    @staticmethod
    async def update_api(db, api_id, update_json):
        if not(api := await ApisService.get_api_by_id(db, api_id)):
            raise Exception("Api not found")

        schema = ApisSchema()
        data = schema.load(update_json)

        for key, value in data.items():
            setattr(api, key, value)

        try:
            await db.commit()
            await db.refresh(api)

        except Exception as e:
            await db.rollback()
            raise e

        return api

    @staticmethod
    async def get_api_by_id(db, api_id):
        sql = select(Apis).where(Apis.id == api_id)
        result = await db.execute(sql)
        api = result.scalars().first()
        return api