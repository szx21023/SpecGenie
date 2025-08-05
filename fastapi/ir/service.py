from main import app
from sqlalchemy import select

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

        return ir
    
    @staticmethod
    async def get_ir(db):
        sql = select(IR)
        result = await db.execute(sql)
        irs = result.scalars().all()

        schema = IRSchema()
        irs = schema.dump(irs, many=True)
        return irs