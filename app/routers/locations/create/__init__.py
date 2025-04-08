from aiogram import Router

from .state_routers.name.handlers import (
    router as name_router
)
from .state_routers.description.handlers import router as des_router
from .state_routers.photo.handlers import router as photo_router
from .state_routers.city.handlers import router as city_router
from .state_routers.street.handlers import router as street_router
from .state_routers.house.handlers import router as house_router
from .state_routers.flat.handlers import router as flat_router
from .state_routers.timezone.handlers import router as timezone_router
from .queue import handler


router = Router()

router.include_routers(
    name_router,
    des_router,
    photo_router,
    city_router,
    street_router,
    house_router,
    flat_router,
    timezone_router,
)
