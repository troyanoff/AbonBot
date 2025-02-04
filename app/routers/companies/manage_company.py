import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, PhotoSize

from filters.general import EmailFilter
from keyboards.inline.base import create_inline_kb
from routers.companies.default import companies_command
from services.clients import get_client_service
from services.companies import get_company_service
from schemas.companies import CompanyCreateSchema
from schemas.representations import ClientReprSchema
from states.general import FSMCompanyCreate, FSMDefault, FSMCompanyRepr


logger = logging.getLogger(__name__)

router = Router()


