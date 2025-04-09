class NotFoundException(Exception):
    """Exception raised when a requested resource is not found."""
    def __init__(self, message="Resource not found"):
        super().__init__(message)


class BadRequestException(Exception):
    """Exception raised for invalid request data."""
    def __init__(self, message="Bad request"):
        super().__init__(message)

class DatabaseException(Exception):
    """Exception raised for database-related errors."""
    def __init__(self, message="A database error occurred"):
        super().__init__(message)