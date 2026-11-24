from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ExtractionError(Exception):
    def __init__(self, message: str, filename: str = "") -> None:
        super().__init__(message)
        self.filename = filename


class UnsupportedFileTypeError(ExtractionError):
    pass


def _error(message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"status": False, "message": message, "data": None},
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ExtractionError)
    async def extraction_error_handler(request: Request, exc: ExtractionError):
        return _error(str(exc), 422)

    @app.exception_handler(UnsupportedFileTypeError)
    async def unsupported_file_handler(request: Request, exc: UnsupportedFileTypeError):
        return _error(str(exc), 415)

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return _error(str(exc), 422)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        return _error("Invalid request payload.", 422)

    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException):
        return _error(exc.detail, exc.status_code)

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        return _error("Something went wrong.", 500)
