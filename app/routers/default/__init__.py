from aiogram import Router

from .default import router as default_router
from .menu import router as menu_router


router = Router()


router.include_routers(
    default_router,
    menu_router,
)
