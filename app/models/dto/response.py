from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: int
    details: str


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Any = None
    errors: list[ErrorResponse] = Field(default_factory=list)