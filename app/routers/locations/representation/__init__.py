from aiogram import Router

from .state_routers.repr.handlers import (
    router as repr_router, handler
)

router = Router()


router.include_routers(
    repr_router,
)
