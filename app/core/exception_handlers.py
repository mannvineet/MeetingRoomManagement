from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def handle_http_exception(request: Request,exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": str(exc.detail),
            "data": {},
            "errors": [
                {
                    "code": exc.status_code,
                    "details": str(exc.detail)
                }
            ]
        }
    )


async def handle_validation_error(request: Request,exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        if error["type"] == "json_invalid":
            errors.append({
                "code": 400,
                "details": "Request body contains invalid JSON"
            })
            continue
        field = ".".join(str(value) for value in error["loc"])

        if error["type"] == "missing":
            errors.append({
                "code": 400,
                "details": (
                    f"Required field "
                    f"'{field.removeprefix('body.')}' is missing"
                )
            })
        else:
            errors.append({
                "code": 422,
                "details": f"{field.removeprefix('body.')}: {error['msg']}"
            })

    status_code = max(error["code"] for error in errors)

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": "Request validation failed",
            "data": {},
            "errors": errors
        }
    )