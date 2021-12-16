from http import HTTPStatus

from starlette.exceptions import HTTPException as StarletteHTTPException


# Why not inherit from Exception https://github.com/tiangolo/fastapi/issues/2750
class FakeCourierException(StarletteHTTPException):
    def __init__(
        self,
        message="An error occurred while processing the request.",
        http_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(status_code=http_code, detail=message)


class NotFoundException(StarletteHTTPException):
    def __init__(self, message: str = "NotFoundException exception."):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=message)


class ExternalApiException(StarletteHTTPException):
    def __init__(self, message: str, http_code: int):
        super().__init__(status_code=http_code, detail=message)
