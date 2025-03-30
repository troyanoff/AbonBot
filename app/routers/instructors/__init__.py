from aiogram import Router

from .representation import router as repr_router
from .create import router as create_router
from .manage import router as manage_router
from .update import router as update_router


router = Router()


router.include_routers(
    repr_router,
    update_router,
    create_router,
    manage_router,
)
