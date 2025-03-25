from aiogram import Router

from .state_routers import (
    first_name, last_name, gender, photo
)


router = Router()


router.include_routers(
    first_name.router,
    last_name.router,
    gender.router,
    photo.router
)
