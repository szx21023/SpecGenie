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
        sql = select(IR).where()
        result = await db.execute(sql)
        irs = result.scalars().all()

        schema = IRSchema()
        irs = schema.dump(irs, many=True)

        for ir in irs:
            for api in ir.get('apis'):
                print(api.get('method'), api.get('path'))
                print(api.get('operation'), api.get('entity'))
                print('Request Fields:', api.get('request_fields'))
                print('Response Fields:', api.get('response_fields'))
                print('-------')

            for entity in ir.get('entities'):
                print(entity.get('name'))
                for field in entity.get('fields'):
                    print(field)
                print('-------')
        return irs