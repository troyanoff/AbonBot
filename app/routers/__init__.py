from aiogram import Router

from routers.auxiliaries import router as auxiliaries_router
from routers.clients import router as clents_router
from routers.default import router as default_router
from routers.companies import router as companies_router
from routers.locations import router as locations_router
from routers.actions import router as actions_router
from routers.subscriptions import router as subs_router
# from routers.instructors import router as instructors_router
# from routers.cards import router as cards_router


router = Router()

router.include_routers(
    default_router,
    # cards_router,
    # instructors_router,
    subs_router,
    actions_router,
    locations_router,
    companies_router,
    clents_router,
    auxiliaries_router,
)
