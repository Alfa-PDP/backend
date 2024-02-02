import logging
from typing import Annotated, TypedDict
from uuid import UUID

import jwt
from fastapi import Depends, Security
from fastapi.security import APIKeyHeader

from app.api.dependencies.configs import MainConfigDep
from app.api.dependencies.services import AuthServiceDep
from app.core import errors
from app.core.config import AuthConfig
from app.schemas.auth import AuthData

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

logger = logging.getLogger().getChild("auth")


class PayloadDict(TypedDict):
    user_id: str


async def authorize_user(
    auth_service: AuthServiceDep,
    config: MainConfigDep,
    access_token: str | None = Security(api_key_header),
) -> AuthData:
    if not access_token:
        raise errors.ForbiddenError

    payload = _validate_token(access_token, config.auth)

    auth_data: AuthData = await auth_service.authorize_user(UUID(payload["user_id"]))
    logger.debug(f"User request: user_id - {auth_data.user_id}")
    return auth_data


def _validate_token(token: str, config: AuthConfig) -> PayloadDict:
    try:
        payload: PayloadDict = jwt.decode(token, config.jwt_secret_key, algorithms=[config.encode_algorithm])
    except (
        jwt.DecodeError,
        jwt.InvalidKeyError,
        jwt.InvalidIssuerError,
        jwt.InvalidSignatureError,
    ):
        logger.error(f"Can't decode jwt token! See {token}")
        raise errors.TokenDecodeError

    except jwt.exceptions.ExpiredSignatureError as error:
        logger.warning(f"Token is expired! error = {error}")
        raise errors.TokenExpiredError

    logger.info(">>> Payload %s", payload)

    return payload


AuthorizeUserDep = Annotated[AuthData, Depends(authorize_user)]
