import logging

from fastapi import FastAPI

from app.core.errors.application import ApplicationError

from .app_handler import application_handler

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, application_handler)
    logger.info("Add %s handler", ApplicationError)
