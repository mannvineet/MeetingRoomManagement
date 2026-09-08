from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_auth_service
from app.helpers.database import get_db
from app.models.db.users import Users
from app.models.dto.auth import Token
from app.models.dto.response import APIResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

# class InitialAdminRequest(BaseModel):
#     name: str = Field(min_length=1)
#     email: EmailStr
#     password: str = Field(min_length=6)
#
#
# @router.post(
#     "/setup-admin",
#     response_model=APIResponse
# )
# async def setup_admin(
#     data: InitialAdminRequest,
#     db: AsyncSession = Depends(get_db)
# ):
#     admin = Users(
#         name=data.name,
#         email=data.email,
#         role="ADMIN",
#         hashed_password=await AuthService.hash_password(
#             data.password
#         )
#     )
#
#     db.add(admin)
#
#     await db.commit()
#
#     return APIResponse(
#         success=True,
#         message="Initial admin created successfully",
#         data={
#             "email": admin.email
#         }
#     )

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
):
    token = await service.login(
        form_data.username,
        form_data.password
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }