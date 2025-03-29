from aiogram import Router

from .state_routers.repr.handlers import router as repr_router

router = Router()


router.include_routers(
    repr_router,
)
