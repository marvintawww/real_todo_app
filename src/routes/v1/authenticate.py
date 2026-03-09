from fastapi import APIRouter, status, Depends

from src.entities.user import UserCreateClient, UserAuthenticate
from src.entities.jwt import TokenPairResponse, RefreshTokenRequest
from src.services.user import UserService
from src.services.jwt import JWTService
from src.dependencies.user import get_user_service
from src.dependencies.jwt import get_jwt_service

router = APIRouter()


@router.post(
    "/register",
    response_model=TokenPairResponse,
    status_code=status.HTTP_200_OK,
    summary="Регистрация",
)
async def register(
    data: UserCreateClient,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> TokenPairResponse:
    user = await user_service.create_user(data)
    return await jwt_service.create_token_pair(user.id)


@router.post(
    "/login",
    response_model=TokenPairResponse,
    status_code=status.HTTP_200_OK,
    summary="Вход",
)
async def login(
    data: UserAuthenticate,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> TokenPairResponse:
    user = await user_service.authenticate(data)
    return await jwt_service.create_token_pair(user.id)


@router.post("/logout", status_code=status.HTTP_200_OK, summary="Выход")
async def logout(
    data: RefreshTokenRequest, jwt_service: JWTService = Depends(get_jwt_service)
) -> dict:
    await jwt_service.logout(data.refresh_token)
    return {"detail": "Успешный выход из аккаунта!"}


@router.post(
    "/refresh",
    response_model=TokenPairResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновление пары токенов",
)
async def refresh_token_pair(
    data: RefreshTokenRequest, jwt_service: JWTService = Depends(get_jwt_service)
) -> TokenPairResponse:
    return await jwt_service.refresh(data.refresh_token)
