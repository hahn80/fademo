#!/usr/bin/env python
# -*- coding: utf-8 -*-


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from myapp.core.event_handlers import lifespan
from myapp.core.config import settings
from myapp.routers.router import api_router
from myapp.database import Base, engine


# from fastapi.openapi.docs import get_swagger_ui_html

# Create the database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.is_debug,
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
def homepage():
    return RedirectResponse(url="/docs")


# Include the main router with all nested routers
app.include_router(api_router)


# Add startup and shutdown event handlers
# @app.on_event("startup")
# async def startup_event():
#     event_handlers.start_app_handler(app)()


# @app.on_event("shutdown")
# async def shutdown_event():
#     event_handlers.stop_app_handler(app)()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
