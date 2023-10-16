class NoRequiredFieldsException(Exception):
    def __init__(self, message: str = "No Required Fields", *args: object) -> None:
        super().__init__(message, *args)


class InvalidFieldTypeException(Exception):
    def __init__(self, message: str = "Invalid Field Type", *args: object) -> None:
        super().__init__(message, *args)


class ConflictException(Exception):
    def __init__(self, message: str = "Conflict", *args: object) -> None:
        super().__init__(message, *args)


class NotFoundException(Exception):
    def __init__(self, message: str = "Not Found", *args: object) -> None:
        super().__init__(message, *args)


class UnauthorizedException(Exception):
    def __init__(self, message: str = "Unauthorized", *args: object) -> None:
        super().__init__(message, *args)


class ForbiddenException(Exception):
    def __init__(self, message: str = "Forbidden", *args: object) -> None:
        super().__init__(message, *args)


class UnprocessableContent(Exception):
    def __init__(self, message: str = "Unprocessable Content", *args: object) -> None:
        super().__init__(message, *args)
