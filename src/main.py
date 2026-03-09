from fastapi import FastAPI
from contextlib import asynccontextmanager
from jose import JWTError
from fastapi.middleware.cors import CORSMiddleware

from src.models.jwt import JWTBlacklist
from src.models.task import Task
from src.models.type import TaskType
from src.models.user import User
from src.database.db import db
from src.routes.v1.__init__ import router as main_router
from src.exceptions.exceptions import ItemNotExist, ItemAlreadyExist, AuthenticateError
from src.exceptions.handlers import (
    item_not_exist_handler,
    item_already_exist_handler,
    authenticate_error_handler,
    jwt_error_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_tables()
    yield
    await db.engine.dispose()


app = FastAPI(
    title="TODO APP", description="TODO APP", version="0.0.1", lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

app.exception_handler(ItemNotExist)(item_not_exist_handler)
app.exception_handler(ItemAlreadyExist)(item_already_exist_handler)
app.exception_handler(AuthenticateError)(authenticate_error_handler)
app.exception_handler(JWTError)(jwt_error_handler)
