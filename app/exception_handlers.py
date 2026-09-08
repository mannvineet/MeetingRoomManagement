from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models.dto.response import APIResponse, ErrorResponse


def handle_http_exception(
    request: Request,
    exc: HTTPException
):
    response = APIResponse(
        success=False,
        message=str(exc.detail),
        data=None,
        errors=[
            ErrorResponse(
                code=exc.status_code,
                details=str(exc.detail)
            )
        ]
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )


def handle_validation_error(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        field = ".".join(
            str(value) for value in error["loc"]
        )
        field = field.removeprefix("body.")

        if error["type"] == "json_invalid":
            errors.append(
                ErrorResponse(
                    code=400,
                    details="Request body contains invalid JSON"
                )
            )
        elif error["type"] == "missing":
            errors.append(
                ErrorResponse(
                    code=400,
                    details=f"Required field '{field}' is missing"
                )
            )
        else:
            errors.append(
                ErrorResponse(
                    code=422,
                    details=f"{field}: {error['msg']}"
                )
            )

    status_code = max(
        error.code for error in errors
    )

    response = APIResponse(
        success=False,
        message="Request validation failed",
        data=None,
        errors=errors
    )

    return JSONResponse(
        status_code=status_code,
        content=response.model_dump()
    )
