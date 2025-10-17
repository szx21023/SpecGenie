from main import app
from sqlalchemy import select

from .schema import DocsPostSchema
from .model import DocsPost

class DocsPostService:
    @staticmethod
    async def get_docs_posts(db):
        # Implementation for getting docs posts
        sql = select(DocsPost)
        result = await db.execute(sql)
        docs_posts = result.scalars().all()

        schema = DocsPostSchema(many=True)
        docs_posts = schema.dump(docs_posts)
        return docs_posts


    @staticmethod
    async def create_docs_post(db, docs_post, **kwargs):
        # Implementation for creating a docs post
        schema = DocsPostSchema()
        data = schema.load(docs_post)

        docs_post = DocsPost(**data)
        db.add(docs_post)
        try:
            await db.commit()
            await db.refresh(docs_post)

        except Exception as e:
            await db.rollback()
            raise e

        return docs_post

    @staticmethod
    async def update_docs_post(db, post_id: int, update_json):
        # Implementation for updating a docs post
        if not(docs_post := await DocsPostService.get_docs_post_by_id(db, post_id)):
            raise Exception("DocsPost not found")

        schema = DocsPostSchema()
        data = schema.load(update_json)

        for key, value in data.items():
            setattr(docs_post, key, value)

        try:
            await db.commit()
            await db.refresh(docs_post)

        except Exception as e:
            await db.rollback()
            raise e

        return docs_post

    @staticmethod
    async def delete_docs_post(db, post_id: int):
        # Implementation for deleting a docs post
        if not (docs_post := await DocsPostService.get_docs_post_by_id(db, post_id)):
            raise Exception("DocsPost not found")

        try:
            await db.delete(docs_post)
            await db.commit()

        except Exception as e:
            await db.rollback()
            raise e

        return docs_post

    @staticmethod
    async def get_docs_post_by_id(db, post_id: int):
        sql = select(DocsPost).where(DocsPost.id == post_id)
        result = await db.execute(sql)
        docs_post = result.scalars().first()
        return docs_post