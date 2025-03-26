from aiogram import Router

from .representation import router as repr_router
from .create import router as create_router


router = Router()


router.include_routers(
    repr_router,
    create_router,
)
