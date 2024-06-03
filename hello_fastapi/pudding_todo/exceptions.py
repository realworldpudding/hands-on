import http
from typing import Any
from fastapi import HTTPException


class DuplicatedError(HTTPException):
    def __init__(self, detail: Any):
        super().__init__(status_code=http.HTTPStatus.BAD_REQUEST, detail=detail)
