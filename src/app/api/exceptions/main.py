import logging

from fastapi import FastAPI

from app.api.exceptions.app_handler import application_handler
from app.core.errors.application import ApplicationError

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Настройка обработчиков исключений для FastAPI приложения.

    Аргументы:
        - app (FastAPI): FastAPI приложение.

    Возвращает:
        - None
    """
    app.add_exception_handler(ApplicationError, application_handler)
    logger.info("Add %s handler", ApplicationError)
