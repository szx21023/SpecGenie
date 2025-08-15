from main import app
from sqlalchemy import select

from .schema import TablesSchema
from .model import Tables

class TablesService:
    @staticmethod
    async def create_table(db, table, **kwargs):
        schema = TablesSchema()
        data = schema.load(table)

        table = Tables(**data)
        db.add(table)
        try:
            await db.commit()
            await db.refresh(table)

        except Exception as e:
            await db.rollback()
            raise e

        return table

    @staticmethod
    async def get_tables(db):
        sql = select(Tables)
        result = await db.execute(sql)
        tables = result.scalars().all()

        schema = TablesSchema(many=True)
        tables = schema.dump(tables)
        return tables
