import logging

from aiogram import Router

from routers.clients import router as clents_router
from routers.default import router as default_router


logger = logging.getLogger(__name__)

router = Router()

logger.info('include all routers')

router.include_routers(
    clents_router,
    default_router,
)
