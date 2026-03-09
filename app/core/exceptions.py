class AppException(Exception):
    """base exception for application"""


class UserNotFoundError(AppException):
    """user not found error"""


class ArticleNotFoundError(AppException):
    """article not found error"""


class AuthorNotFoundError(AppException):
    """author not found error"""


class ArticlesNotFoundError(AppException):
    """articles not found error"""


class TeamsNotFoundError(AppException):
    """teams not found error"""


class AuthenticationError(AppException):
    """user not authenticated"""
    pass
