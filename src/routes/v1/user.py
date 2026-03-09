from fastapi import Depends, APIRouter, status

from src.dependencies.user import get_user_service
from src.dependencies.authenticate import get_current_user
from src.entities.user import UserResponse
from src.services.user import UserService


router = APIRouter()


@router.get(
    "/profile",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Профиль пользователя",
)
async def get_profile(
    current_user: dict = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    user_id = int(current_user.get("sub"))
    return await user_service.get_user(user_id)
