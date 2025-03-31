import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb
from schemas.representations import SubscriptionListSchema
from schemas.subscriptions import SubscriptionCreateSchema
from schemas.utils import FailSchema, DoneSchema
from services.clients import get_client_service
from services.subscriptions import get_subscription_service
from routers.subscriptions.create.state import states_group
from routers.default.state import FSMDefault
from .terminology import terminology, Lang


logger = logging.getLogger(__name__)

router = Router()
router_state = states_group.client


async def start(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:start'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    data = await state.get_data()

    await callback.answer()
    await state.update_data(
        new_sub={
            'company_uuid': data['company_uuid']
        }
    )

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *states_group.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await callback.message.answer(
        text=terminology_lang.terms.start_create,
        reply_markup=keyboard
    )
    await state.set_state(router_state)


@router.message(
    StateFilter(router_state),
    F.text.regexp(r'^\d+$')
)
async def done(
    message: Message, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:done'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    client_service = get_client_service()
    client = await client_service.get(int(message.text))

    if isinstance(client, FailSchema) and client.response.status == 404:
        core_buttons = await core_term_lang.buttons.get_dict_with(
            *states_group.core_buttons)

        keyboard = await create_simply_inline_kb(
            core_buttons,
            1
        )
        await message.answer(
            text=terminology_lang.terms.not_found,
            reply_markup=keyboard
        )

    if isinstance(client, FailSchema):
        await message.answer(
            text=core_term_lang.terms.error
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    data = await state.get_data()
    new_sub_dict = data['new_sub']
    new_sub_dict['client_uuid'] = client.uuid

    service = get_subscription_service()

    actual_sub = await service.get_list(
        **new_sub_dict
    )

    if isinstance(actual_sub, FailSchema):
        await message.answer(
            text=core_term_lang.terms.error
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    if (isinstance(actual_sub, SubscriptionListSchema)
            and actual_sub.total_count > 0):
        del data['new_sub']
        await state.update_data(**data)
        await message.answer(
            text=terminology_lang.terms.already_exist
        )
        from routers.subscriptions.representation_company.state_routers.repr.\
            handlers import start

        await start(message=message, lang=lang, state=state)
        return

    result = await service.create(
        SubscriptionCreateSchema.model_validate(new_sub_dict))

    if isinstance(result, FailSchema):
        await message.answer(
            text=core_term_lang.terms.error
        )
        await state.clear()
        await state.set_state(FSMDefault.default)
        return

    del data['new_sub']
    await state.update_data(**data)
    from routers.subscriptions.representation_company.state_routers.repr.\
        handlers import start

    await start(message=message, lang=lang, state=state)


@router.callback_query(
    StateFilter(router_state),
    F.data == 'back_state'
)
async def back_state(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str
):
    state_handler = f'{router_state.state}:back_state'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    from routers.companies.manage.state_routers.default.handlers \
        import manage
    data = await state.get_data()
    await manage(
        message=callback.message, state=state, lang=lang,
        uuid=data['company_uuid'],
        edit_text=True
    )


@router.message(
    StateFilter(router_state)
)
async def error(
    message: Message, lang: str
):
    state_handler = f'{router_state.state}:error'
    logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    core_buttons = await core_term_lang.buttons.get_dict_with(
        *states_group.core_buttons)

    keyboard = await create_simply_inline_kb(
        core_buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.error,
        reply_markup=keyboard
    )
