class AppError(Exception):
    status_code: int = 500
    code: str = "internal_error"
    message: str = "Internal server error"

    def __init__(self, message: str | None = None, code: str | None = None, **extra):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.extra = extra
        super().__init__(self.message)


class BadRequestError(AppError):
    status_code = 400
    code = "bad_request"
    message = "Bad request"


class UnauthorizedError(AppError):
    status_code = 401
    code = "unauthorized"
    message = "Authentication required"


class ForbiddenError(AppError):
    status_code = 403
    code = "forbidden"
    message = "Permission denied"


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"
    message = "Resource not found"


class ConflictError(AppError):
    status_code = 409
    code = "conflict"
    message = "Resource conflict"


class TooManyRequestsError(AppError):
    status_code = 429
    code = "too_many_requests"
    message = "Too many requests"