from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_auth_service
from app.schemas.auth import Token
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(form_data.username,form_data.password)

# class InitialAdminRequest(BaseModel):
#     name: str
#     email: str
#     password: str


# @router.post("/setup-admin")
# async def setup_admin(data: InitialAdminRequest,db: AsyncSession = Depends(get_db)):
#     admin = Users(
#         name=data.name,
#         email=data.email,
#         role="ADMIN",
#         hashed_password=hash_password(data.password)
#     )
#
#     db.add(admin)
#     await db.commit()
#     await db.refresh(admin)
#
#     return {"message": "Initial admin created","email": admin.email}