from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core import errors


async def application_handler(_: Request, exception: errors.ApplicationError) -> JSONResponse:
    content = {
        "error_code": exception.error_code,
        "error_message": exception.error_message,
    }

    if isinstance(exception, errors.BaseNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exception, errors.BaseAuthError):
        status_code = status.HTTP_403_FORBIDDEN
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
