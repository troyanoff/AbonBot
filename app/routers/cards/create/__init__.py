from aiogram import Router

from .state_routers.name.handlers import router as name_router
from .state_routers.description.handlers import router as des_router
from .state_routers.by_delta.handlers import router as by_delta_router
from .state_routers.month_delta.handlers import router as month_delta_router
from .state_routers.by_count.handlers import router as by_count_router
from .state_routers.count.handlers import router as count_router
from .state_routers.by_limit.handlers import router as by_limit_router
from .state_routers.time_limit.handlers import router as time_limit_router
from .state_routers.freeze.handlers import router as freeze_router
from .state_routers.freezing_days.handlers import \
    router as freezing_days_router
from .state_routers.location.handlers import router as location_router
from .state_routers.actions.handlers import router as actions_router
from .state_routers.general.handlers import router as general_router


router = Router()

router.include_routers(
    name_router,
    des_router,
    by_delta_router,
    month_delta_router,
    by_count_router,
    count_router,
    by_limit_router,
    time_limit_router,
    freeze_router,
    freezing_days_router,
    location_router,
    actions_router,
    general_router,
)
