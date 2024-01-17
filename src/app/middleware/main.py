import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.middleware.request_id import RequestIdHeaderMiddleware

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestIdHeaderMiddleware)
