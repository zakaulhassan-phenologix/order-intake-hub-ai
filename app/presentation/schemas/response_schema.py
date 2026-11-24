"""
Final response schema used by EVERY endpoint.

Every route returns:
    {
        "message": "...",
        "status": "success" | "error",
        "data": <payload or null>
    }
"""

from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class ApiResponse(BaseModel, Generic[T]):
    message: str
    status: ResponseStatus
    data: Optional[T] = None

    @classmethod
    def success(cls, data: Optional[T] = None, message: str = "OK") -> "ApiResponse[T]":
        return cls(message=message, status=ResponseStatus.SUCCESS, data=data)

    @classmethod
    def error(cls, message: str, data: Optional[T] = None) -> "ApiResponse[T]":
        return cls(message=message, status=ResponseStatus.ERROR, data=data)
