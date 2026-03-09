from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import JWTError

from src.exceptions.exceptions import ItemAlreadyExist, ItemNotExist, AuthenticateError


async def item_not_exist_handler(request: Request, exc: ItemNotExist):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Объект не найден"}
    )


async def item_already_exist_handler(request: Request, exc: ItemAlreadyExist):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Объект уже существует"},
    )


async def authenticate_error_handler(request: Request, exc: AuthenticateError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Ошибка аутентификации"},
    )


async def jwt_error_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Ошибка авторизации"},
    )
