from main import app
from sqlalchemy import select

from apis.service import ApisService
from tables.service import TablesService
from .schema import IRSchema
from .model import IR

class IRService: 
    @staticmethod
    async def create_ir(db, ir, **kwargs):
        schema = IRSchema()
        data = schema.load(ir)

        ir = IR(**data)
        db.add(ir)
        try:
            await db.commit()
            await db.refresh(ir)

        except Exception as e:
            await db.rollback()
            raise e

        return data

    @staticmethod
    async def get_ir(db):
        apis = await ApisService.get_apis(db)
        tables = await TablesService.get_tables(db)

        schema = IRSchema()
        irs = schema.load({'apis': apis, 'entities': tables})
        return irs
