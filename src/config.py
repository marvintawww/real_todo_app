import os

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/todo"
SECRET = os.getenv("SECRET_KEY", "defualt-key")
