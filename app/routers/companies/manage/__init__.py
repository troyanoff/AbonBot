from aiogram import Router

from .state_routers.default.handlers import router as default_router
from .state_routers.comands.handlers import router as comands_router


router = Router()

router.include_routers(
    default_router,
    comands_router,
)
