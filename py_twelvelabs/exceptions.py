
class MissingAPIKeyError(Exception):
    """
    Raised when an API key is not provided.
    """
    pass


class MethodNotImplementedError(Exception):
    """
    Raised when a method is not implemented.
    """
    pass


class APIRequestError(Exception):
    """
    Raised when an API request fails.
    """
    pass


class InsufficientParametersError(Exception):
    """
    Raised when insufficient parameters are provided.
    """
    pass


class TaskDeletionNotAllowedError(Exception):
    """
    Raised when a task deletion is not allowed.
    """
    pass


class TaskFailedError(Exception):
    """
    Raised when a task fails.
    """
    pass