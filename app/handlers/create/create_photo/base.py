from aiogram import F
from aiogram.filters import StateFilter

from handlers.create.base import CreateConfig, CreateField


class CreateFieldPhoto(CreateField):
    def __init__(
        self,
        config: CreateConfig
    ):
        self.config = config
        self._register_handlers()

    def _register_mutable_handlers(self):
        self.config.router.message(
            StateFilter(self.config.router_state),
            F.photo[-1].as_('largest_photo')
        )(self.done)
        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.in_(self.config.states_group.photo_callbacks)
        )(self.cancel)

    async def update_data(self):
        return await super().update_data(message, state)

@router.message(
    StateFilter(router_state),
    F.photo[-1].as_('largest_photo')
)
async def done(
    message: Message, state: FSMContext, lang: str,
    largest_photo: PhotoSize
):
    state_handler = f'{router_state.state}:done'
    logger.info(state_handler)

    data = await state.get_data()

    new_location_dict = data['new_location']
    new_location_dict['photo_unique_id'] = largest_photo.file_unique_id
    new_location_dict['photo_id'] = largest_photo.file_id
    await state.update_data(
        new_location=new_location_dict
    )

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    buttons = await core_term_lang.buttons.get_dict_with(
        *router_group.core_buttons)

    keyboard = await create_simply_inline_kb(
        buttons,
        1
    )
    await message.answer(
        text=terminology_lang.terms.done,
        reply_markup=keyboard
    )
    await state.set_state(next_state)


@router.callback_query(
    StateFilter(router_state),
    F.data.in_(router_group.photo_callbacks)
)
async def cancel(
    callback: CallbackQuery, state: FSMContext, lang: str
):
    state_handler = f'{router_state.state}:cancel'
    logger.info(state_handler)

    data = await state.get_data()

    new_location_dict = data['new_location']
    new_location_dict['photo_unique_id'] = ''
    new_location_dict['photo_id'] = ''
    await state.update_data(
        new_location=new_location_dict
    )

    if await st.is_debag():
        data = await state.get_data()
        logger.info(f'{state_handler} {data=}')

    terminology_lang: Lang = getattr(terminology, lang)
    core_term_lang: core_Lang = getattr(core_term, lang)

    buttons = await core_term_lang.buttons.get_dict_with(
        *router_group.core_buttons)

    keyboard = await create_simply_inline_kb(
        buttons,
        1
    )
    await callback.message.answer(
        text=terminology_lang.terms.done,
        reply_markup=keyboard
    )
    await state.set_state(next_state)

