from fastapi import APIRouter

from src.routes.v1.authenticate import router as auth_router
from src.routes.v1.user import router as user_router
from src.routes.v1.type import router as type_router
from src.routes.v1.task import router as task_router


router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(type_router)
router.include_router(task_router)
