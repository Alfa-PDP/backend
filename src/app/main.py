from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.main import setup_routers
from app.core.config import MainConfig
from app.core.logger import setup_logging
from app.middleware.main import setup_middleware
from app.providers.main import setup_providers


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


def main() -> FastAPI:
    config = MainConfig()
    return create_app(config)
