from aiogram import Router

from .representation import router as repr_router
from .create import router as create_router
from .manage import router as manage_router


router = Router()


router.include_routers(
    repr_router,
    manage_router,
    create_router,
)
