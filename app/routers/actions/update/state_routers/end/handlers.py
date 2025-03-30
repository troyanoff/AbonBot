import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.terminology import terminology as core_term, Lang as core_Lang
from routers.actions.create.state import states_group
from routers.actions.manage.state_routers.default.handlers import manage
from routers.default.state import FSMDefault
from schemas.actions import ActionUpdateSchema
from schemas.utils import FailSchema
from services.actions import get_action_service
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.name
next_state = states_group.description


async def end_state(
    message: Message, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:end_state'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    data = await state.get_data()
    update_action = data['update_action']

    service = get_action_service()
    result = await service.update(
        ActionUpdateSchema.model_validate(update_action))

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    if isinstance(result, FailSchema):
        await message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    await message.answer(
        text=terminology_lang.terms.done,
        reply_markup=None
    )
    del data['update_action']
    await state.update_data(**data)

    item = await service.get(result.response.data['item']['uuid'])
    await manage(
        message=message, lang=lang, state=state, item=item
    )
