from aiogram import Router

from .state_routers.name.handlers import router as name_router
from .state_routers.description.handlers import router as des_router
from .state_routers.email.handlers import router as email_router
from .state_routers.photo.handlers import router as photo_router
from .state_routers.max_hour_cancel.handlers import router as hour_router


router = Router()

router.include_routers(
    name_router,
    des_router,
    email_router,
    photo_router,
    hour_router,
)
