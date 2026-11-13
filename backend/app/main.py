from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, system, inbox, agent
from app.core.config import settings
from app.core.error_handlers import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.api import auth, system, inbox, agent, actions, analytics, tasks # <-- Add actions


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    log = get_logger(__name__)
    log.info("app_startup", env=settings.ENVIRONMENT, name=settings.APP_NAME)
    yield
    log.info("app_shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)

    # Register Routers
    app.include_router(system.router, prefix="/api", tags=["system"])
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(inbox.router, prefix="/api/inbox", tags=["inbox"])
    app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
    app.include_router(actions.router, prefix="/api/actions", tags=["actions"])
    app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
    app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
    return app


app = create_app()