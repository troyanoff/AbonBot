from aiogram import Router

from .default import router as default_router


router = Router()


router.include_routers(
    default_router,
)
