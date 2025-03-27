from aiogram import Router

from routers.auxiliaries import router as auxiliaries_router
from routers.clients import router as clents_router
from routers.default import router as default_router
from routers.companies import router as companies_router


router = Router()

router.include_routers(
    companies_router,
    clents_router,
    default_router,
    auxiliaries_router,
)
