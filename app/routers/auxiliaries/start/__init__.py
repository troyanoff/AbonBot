from aiogram import Router

from .state_routers.start.handlers import router as start_router


router = Router()

router.include_routers(
    start_router,
)
