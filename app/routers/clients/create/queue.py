from aiogram import Bot

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from handlers.base import RequestTG
from handlers.remember.base import RememberConfig, Remember
from keyboards.menu.base import set_client_menu
from schemas.base import RememberTypeEnum
from schemas.clients import ClientCreateSchema
from services.clients import get_client_service
from .state_routers.first_name.handlers import handler as fn_h
from .state_routers.last_name.handlers import handler as ln_h
from .state_routers.sex.handlers import handler as sex_h
from .state_routers.photo.handlers import handler as photo_h


async def set_new_client_menu(request_tg: RequestTG):
    bot = Bot(token=st.bot_token)
    core_lang: core_Lang = getattr(core_term, request_tg.lang)
    await set_client_menu(
        bot, request_tg.update.from_user.id, core_lang.menu)


config = RememberConfig(
    remember_type=RememberTypeEnum.create,
    item_prefix='client',
    service_caller=get_client_service,
    schema=ClientCreateSchema,
    queue=[fn_h, ln_h, sex_h, photo_h],
    manage_caller=(
        'routers.clients.profile.state_routers.default.handlers.handler'
    ),
    exists_fields=(('tg_id', None), ),
    additional_end_func=set_new_client_menu
)

handler = Remember(
    config=config
)
