from app.core.errors.application import ApplicationError, BaseErrorEnum

ERROR_CODE = "AccessDenied"


class AuthErrorMessages(BaseErrorEnum):
    base_error = ERROR_CODE, "Ошибка авторизации"
    forbidden_error = ERROR_CODE, "Доступ запрещён"
    token_decode_error = ERROR_CODE, "Проверьте токен доступа"
    token_expired_error = ERROR_CODE, "Срок действия вашего токена истёк"


class BaseAuthError(ApplicationError):
    error_code: str = AuthErrorMessages.base_error.error_code
    error_message: str = AuthErrorMessages.base_error.error_message


class ForbiddenError(BaseAuthError):
    error_message = AuthErrorMessages.forbidden_error.error_code
    error_message = AuthErrorMessages.forbidden_error.error_message


class TokenDecodeError(BaseAuthError):
    error_message = AuthErrorMessages.token_decode_error.error_code
    error_message = AuthErrorMessages.token_decode_error.error_message


class TokenExpiredError(BaseAuthError):
    error_message = AuthErrorMessages.token_decode_error.error_code
    error_message = AuthErrorMessages.token_expired_error.error_message
