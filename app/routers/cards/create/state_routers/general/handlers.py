import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from routers.cards.create.state import states_group
from routers.companies.manage.state_routers.default.handlers import manage


logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(
    StateFilter(*states_group.__all_states__),
    F.data == 'cancel'
)
async def cancel(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{states_group}:cancel'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    data = await state.get_data()
    back_uuid = data['company_uuid']
    await manage(
        message=callback.message, state=state, lang=lang,
        uuid=back_uuid,
        edit_text=True
    )
