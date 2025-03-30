from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.terminology import terminology as core_term, Lang as core_Lang
from routers.default.state import FSMDefault
from schemas.utils import FailSchema
from services.instructors import get_instructor_service
from .terminology import terminology, Lang


async def archive(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    data = await state.get_data()
    instructor_uuid = data['instructor_uuid']

    service = get_instructor_service()
    result = await service.archive(instructor_uuid)
    if isinstance(result, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await callback.message.answer(
            text=core_term_lang.terms.error
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    terminology_lang: Lang = getattr(terminology, lang)
    await callback.answer(text=terminology_lang.terms.archived)
    from routers.instructors.representation.state_routers.repr.handlers \
        import start
    await start(
        callback=callback, state=state, lang=lang
    )
