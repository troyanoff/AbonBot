from aiogram import Router

from .create import router as create_router
from .update import router as update_router


router = Router()


router.include_routers(
    create_router,
    update_router,
)
