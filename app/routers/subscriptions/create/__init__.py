from aiogram import Router

from .state_routers.client.handlers import router as client_router
from .queue import handler

router = Router()


router.include_routers(
    client_router,
)
