from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: int
    details: str


class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict[str, Any]
    errors: list[ErrorDetail] = Field(default_factory=list)