from aiogram import Router

from .state_routers.default.handlers import (
    router as default_router, handler
)


router = Router()

router.include_routers(
    default_router,
)
