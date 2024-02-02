from app.core.errors.application import ApplicationError, BaseErrorEnum

ERROR_CODE = "NotFound"


class NotFoundErrorMessages(BaseErrorEnum):
    base_error = ERROR_CODE, "Запрашиваемый ресурс не найден. Необходимо проверить корректность URL"
    user_not_in_team = ERROR_CODE, "Пользователь не состоит в команде"
    team_not_found = ERROR_CODE, "Команда не найдена"
    user_not_found = ERROR_CODE, "Пользователь не найден"
    idp_not_found = ERROR_CODE, "ИПР сотрудника не найден"
    task_not_found = ERROR_CODE, "Задача не найдена"
    task_status_not_found = ERROR_CODE, "Статус не найден"


class BaseNotFoundError(ApplicationError):
    error_code: str = NotFoundErrorMessages.base_error.error_code
    error_message: str = NotFoundErrorMessages.base_error.error_message


class UserNotInTeamError(BaseNotFoundError):
    error_code: str = NotFoundErrorMessages.user_not_in_team.error_code
    error_message: str = NotFoundErrorMessages.user_not_in_team.error_message


class TeamNotFoundError(BaseNotFoundError):
    error_code: str = NotFoundErrorMessages.team_not_found.error_code
    error_message: str = NotFoundErrorMessages.team_not_found.error_message


class UserNotFoundError(BaseNotFoundError):
    error_code: str = NotFoundErrorMessages.user_not_found.error_code
    error_message: str = NotFoundErrorMessages.user_not_found.error_message


class IDPNotFoundError(BaseNotFoundError):
    error_code: str = NotFoundErrorMessages.idp_not_found.error_code
    error_message: str = NotFoundErrorMessages.idp_not_found.error_message


class TaskNotFoundError(BaseNotFoundError):
    error_code: str = NotFoundErrorMessages.task_not_found.error_code
    error_message: str = NotFoundErrorMessages.task_not_found.error_message


class TaskStatusNotFoundError(BaseNotFoundError):
    error_code: str = NotFoundErrorMessages.task_status_not_found.error_code
    error_message: str = NotFoundErrorMessages.task_status_not_found.error_message
