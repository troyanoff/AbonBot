from aiogram import Router

from .representation_company import router as repr_company_router
from .create import router as create_router
from .manage_company import router as manage_router


router = Router()


router.include_routers(
    repr_company_router,
    create_router,
    manage_router,
)
