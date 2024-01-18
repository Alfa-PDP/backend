from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.dependencies.configs import get_main_config
from app.api.middlewares.main import setup_middleware
from app.api.providers.main import setup_providers
from app.api.routers.main import setup_routers
from app.core.config import MainConfig
from app.core.logger import setup_logging


def create_app(config: MainConfig) -> FastAPI:
    app = FastAPI(
        title=config.project.name,
        docs_url=config.project.docs_url,
        openapi_url=config.project.openapi_url,
        default_response_class=ORJSONResponse,
        description=config.project.description,
        version=config.project.version,
    )

    setup_logging(config)
    setup_providers(app, config)
    setup_routers(app, config)
    setup_middleware(app)
    return app


def main(config: MainConfig = get_main_config()) -> FastAPI:
    return create_app(config)
