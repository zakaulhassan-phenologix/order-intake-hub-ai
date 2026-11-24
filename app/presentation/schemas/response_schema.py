from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    status: bool
    message: str
    data: Optional[T] = None

    @classmethod
    def success(cls, data=None, message: str = "OK") -> "ResponseSchema":
        return cls(status=True, message=message, data=data)

    @classmethod
    def error(cls, message: str, data=None) -> "ResponseSchema":
        return cls(status=False, message=message, data=data)


ApiResponse = ResponseSchema
