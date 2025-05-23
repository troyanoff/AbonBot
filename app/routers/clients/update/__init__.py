from aiogram import Router

from .state_routers.first_name.handlers import router as fn_router
from .state_routers.last_name.handlers import router as ln_router
from .state_routers.sex.handlers import router as gender_router
from .state_routers.photo.handlers import router as photo_router
from .queue import handler


router = Router()

router.include_routers(
    fn_router,
    ln_router,
    gender_router,
    photo_router
)
