from app.core.errors.application import ApplicationError, BaseErrorEnum

ERROR_CODE = "AlreadyExists"


class AlreadyExistsErrorMessages(BaseErrorEnum):
    base_error = ERROR_CODE, "Создаваемый ресурс уже существует"
    goal_already_exists_error = ERROR_CODE, "Цель уже существует"


class BaseAlreadyExistsError(ApplicationError):
    error_code: str = AlreadyExistsErrorMessages.base_error.error_code
    error_message: str = AlreadyExistsErrorMessages.base_error.error_message


class GoalAlreadyExistsError(BaseAlreadyExistsError):
    error_code: str = AlreadyExistsErrorMessages.goal_already_exists_error.error_code
    error_message: str = AlreadyExistsErrorMessages.goal_already_exists_error.error_message
