class ApplicationError(Exception):
    """Base application error"""


class BaseForbiddenError(ApplicationError):
    """Base Auth Exception"""


class TokenDecodeError(ApplicationError):
    """Token Decode Error"""


class TokenExpiredError(ApplicationError):
    """Token expired error"""


class BaseNotFoundError(ApplicationError):
    """Base not found exception"""


class UserNotInTeamError(BaseNotFoundError):
    """User not a member of the team"""


class TeamNotFoundError(BaseNotFoundError):
    """Team not found exception"""


class UserNotFoundError(BaseNotFoundError):
    """User not found exception"""


class IDPNotFoundError(BaseNotFoundError):
    """IDP not found exception"""


class TaskNotFoundError(BaseNotFoundError):
    """Task not found exception"""


class TaskStatusNotFoundError(BaseNotFoundError):
    """Status not found exception"""
