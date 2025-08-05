async def init_app(app):
    from .controller import router

    app.include_router(router)