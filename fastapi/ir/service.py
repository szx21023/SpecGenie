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
        # sql = select(IR)
        # result = await db.execute(sql)
        # irs = result.scalars().all()

        # schema = IRSchema()
        # irs = schema.dump(irs, many=True)
        # return irs

        return [
            {
                'id': 'node-1',
                'type': 'myNode',
                'position': { 'x': 0, 'y': 0 },
                'data': { 
                    'name': 'user',
                    'row': [
                        { 'field': 'name', 'type': 'string', 'value': 'Alice' },
                        { 'field': 'age', 'type': 'integer', 'value': '25' },
                        { 'field': 'job', 'type': 'string', 'value': 'Engineer' }
                    ]
                }
            },
            {
                'id': 'node-2',
                'type': 'myNode',
                'position': { 'x': 0, 'y': 100 },
                'data': { 
                    'name': 'customer',
                    'row': [
                        { 'field': 'name', 'type': 'string', 'value': 'Herry' },
                        { 'field': 'age', 'type': 'integer', 'value': '30' },
                        { 'field': 'job', 'type': 'string', 'value': 'PM' }
                    ]
                }
            },
            {
                'id': 'node-3',
                'type': 'myNode',
                'position': { 'x': 0, 'y': 200 },
                'data': { 
                    'name': 'worker',
                    'row': [
                        { 'field': 'name', 'type': 'string', 'value': 'Judy' },
                        { 'field': 'age', 'type': 'integer', 'value': '18' },
                        { 'field': 'job', 'type': 'string', 'value': 'QA' }
                    ]
                }
            }
        ]