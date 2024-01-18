from fastapi import APIRouter

from app.api.routers.v1.status import router as status_router
from app.api.routers.v1.users import router as users_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(status_router)
v1_router.include_router(users_router)
