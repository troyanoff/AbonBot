from aiogram import Router

from .state_routers.first_name.handlers import router as fn_router
from .state_routers.last_name.handlers import router as ln_router
from .state_routers.sex.handlers import router as sex_router
from .state_routers.photo.handlers import router as photo_router


router = Router()

router.include_routers(
    fn_router,
    ln_router,
    sex_router,
    photo_router
)
