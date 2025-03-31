from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.terminology import terminology as core_term, Lang as core_Lang
from routers.default.state import FSMDefault
from schemas.utils import FailSchema
from services.cards import get_card_service
from .terminology import terminology, Lang


async def archive(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    data = await state.get_data()
    card_uuid = data['card_uuid']

    service = get_card_service()
    result = await service.archive(card_uuid)
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
    from routers.cards.representation.state_routers.repr.handlers \
        import start
    await start(
        message=callback.message, state=state, lang=lang
    )
