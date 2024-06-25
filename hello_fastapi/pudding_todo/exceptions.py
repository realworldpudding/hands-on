import http
from typing import Any
from fastapi import HTTPException


class DuplicatedError(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=http.HTTPStatus.BAD_REQUEST, detail=detail)


class PermissionDenidedError(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=http.HTTPStatus.FORBIDDEN, detail=detail)
