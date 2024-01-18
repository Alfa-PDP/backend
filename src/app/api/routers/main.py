from fastapi import APIRouter, FastAPI

from app.api.routers.v1 import v1_router
from app.core.config import MainConfig


def setup_routers(app: FastAPI, config: MainConfig) -> None:
    root_router = APIRouter(prefix=config.project.api_prefix)
    root_router.include_router(v1_router)
    app.include_router(root_router)
