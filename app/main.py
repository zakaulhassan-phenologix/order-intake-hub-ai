from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.presentation.api.routes.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create clients, load prompts, warm connections
    yield
    # Shutdown: close clients


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
