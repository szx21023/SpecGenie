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

    @staticmethod
    async def update_table(db, table_id, update_json):
        if not(table := await TablesService.get_table_by_id(db, table_id)):
            raise Exception("Table not found")

        schema = TablesSchema()
        data = schema.load(update_json)

        for key, value in data.items():
            setattr(table, key, value)

        try:
            await db.commit()
            await db.refresh(table)

        except Exception as e:
            await db.rollback()
            raise e

        return table

    @staticmethod
    async def delete_table(db, table_id):
        if not (table := await TablesService.get_table_by_id(db, table_id)):
            raise Exception("Table not found")

        try:
            await db.delete(table)
            await db.commit()

        except Exception as e:
            await db.rollback()
            raise e

        return table

    @staticmethod
    async def get_table_by_id(db, table_id):
        sql = select(Tables).where(Tables.id == table_id)
        result = await db.execute(sql)
        table = result.scalars().first()
        return table
