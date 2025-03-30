import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.terminology import terminology as core_term, Lang as core_Lang
from routers.instructors.manage.state_routers.default.handlers import manage
from routers.default.state import FSMDefault
from schemas.instructors import InstructorCreateSchema
from schemas.utils import FailSchema
from services.instructors import get_instructor_service
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)


async def end_create(
    message: Message, state: FSMContext, lang: str
):
    now_state = await state.get_state()
    state_handler = f'{now_state}:end_create'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    data = await state.get_data()
    new_instructor = data['new_instructor']

    service = get_instructor_service()
    result = await service.create(
        InstructorCreateSchema.model_validate(new_instructor))

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
    del data['new_instructor']
    await state.update_data(**data)

    item = await service.get(result.response.data['item']['uuid'])
    await manage(
        message=message, lang=lang, state=state, item=item
    )
