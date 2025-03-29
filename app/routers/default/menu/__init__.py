from aiogram import Router

from .state_routers.general.handlers import router as general_router


router = Router()

router.include_routers(
    general_router,
)
