from aiogram import Router

from .state_routers.client.handlers import router as client_router

router = Router()


router.include_routers(
    client_router,
)
