from aiogram import Router

from .deadlock import router as router_


router = Router()

router.include_routers(
    router_,
)
