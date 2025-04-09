from aiogram import Router

from .state_routers.name.handlers import router as name_router
from .state_routers.description.handlers import router as des_router
from .state_routers.photo.handlers import router as photo_router
from .queue import handler


router = Router()

router.include_routers(
    name_router,
    des_router,
    photo_router,
)
