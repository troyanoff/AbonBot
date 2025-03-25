from aiogram import Router

from .start import router as start_router
from .deadlock import router as deadlock_router


router = Router()


router.include_routers(
    start_router,
    deadlock_router,
)
