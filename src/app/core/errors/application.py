import enum


class BaseErrorEnum(enum.Enum):
    @property
    def error_code(self) -> str:
        return self.value[0]

    @property
    def error_message(self) -> str:
        return self.value[1]


class ApplicationErrorMessages(BaseErrorEnum):
    base_error = "ApplicationError", "Something Went Wrong"


class ApplicationError(Exception):
    """Base application error"""

    error_code: str = ApplicationErrorMessages.base_error.error_code
    error_message: str = ApplicationErrorMessages.base_error.error_message

    def __init__(self) -> None:
        super().__init__(self.error_message)
