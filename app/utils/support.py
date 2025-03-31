from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.terminology import terminology as core_term, Lang as core_Lang
from routers.default.state import FSMDefault
from schemas.utils import DoneSchema, FailSchema


async def bad_response(
    message: Message, state: FSMContext,
    lang: str, response: DoneSchema | FailSchema
) -> bool:
    if isinstance(response, FailSchema):
        core_term_lang: core_Lang = getattr(core_term, lang)
        await message.answer(
            text=core_term_lang.terms.error,
            reply_markup=None
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return
