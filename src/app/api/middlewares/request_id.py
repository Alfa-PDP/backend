from fastapi import status
from fastapi.responses import ORJSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request


class RequestIdHeaderMiddleware(BaseHTTPMiddleware):
    """
    Промежуточное ПО для добавления проверки X-Request-Id заголовка в запросы.

    Аргументы:
        - request (Request): Запрос FastAPI.
        - call_next (RequestResponseEndpoint): Следующий обработчик запроса.

    Возвращает:
        - Response: Ответ FastAPI.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            content = {"detail": "X-Request-Id is required"}
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
        return response
