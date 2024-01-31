class ApplicationError(Exception):
    """Base application error"""


class BaseForbiddenError(ApplicationError):
    """Base Auth Exception"""


class TokenDecodeError(ApplicationError):
    """Token Decode Error"""


class TokenExpiredError(ApplicationError):
    """Token expired error"""


class UserNotInTeamError(ApplicationError):
    """User not a member of the team"""
