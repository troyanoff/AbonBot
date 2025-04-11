from aiogram import Router

from .state_routers.photo.handlers import router as photo_router
from .queue import handler

router = Router()


router.include_routers(
    photo_router,
)
