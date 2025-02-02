
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards.inline.base import create_inline_kb
from keyboards.inline.factories import company_inline
from services.companies import get_company_service
from states.general import FSMClientUpdate, FSMStart, FSMDefault
from schemas.representations import ClientReprSchema


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(
    message: Message,
    state: FSMContext,
    i18n: dict,
    client_data: ClientReprSchema | None
):
    if not client_data:
        await message.answer(
            text=i18n['phrases']['start_unknow']
        )
        await state.set_state(FSMStart.start)
        return

    await message.answer(
        text=i18n['phrases']['start']
    )


@router.message(Command(commands='learn'), StateFilter(FSMDefault.default))
async def learn_command(
    message: Message,
    i18n: dict
):
    await message.answer(
        text=i18n['phrases']['learn']
    )


@router.message(Command(commands='support'), StateFilter(FSMDefault.default))
async def support_command(
    message: Message,
    i18n: dict
):
    await message.answer(
        text=i18n['phrases']['support']
    )


@router.message(Command(commands='profile'), StateFilter(FSMDefault.default))
async def profile_command(
    message: Message,
    i18n: dict,
    client_data: ClientReprSchema
):
    buttons_list = ('update_profile', )
    keyboard = await create_inline_kb(
        i18n['buttons'], 1,
        *buttons_list,
        cancel_button=False
    )
    sex = i18n['phrases'][f'gender_{client_data.sex.name}']
    text = i18n['phrases']['profile'].format(
        first_name=client_data.first_name,
        last_name=client_data.last_name,
        sex=sex,
        companies_count=client_data.companies_count,
        subs_count=client_data.subs_count
    )
    if not client_data.photo_id:
        await message.answer(
            text=text,
            reply_markup=keyboard
        )
        return
    await message.answer_photo(
        photo=client_data.photo_id,
        caption=text,
        reply_markup=keyboard
    )


@router.callback_query(
    StateFilter(FSMDefault.default),
    F.data == 'update_profile'
)
async def update_profile(
    callback: CallbackQuery,
    state: FSMContext,
    i18n: dict
):
    buttons_list = ('cancel', )
    keyboard = await create_inline_kb(
        i18n['buttons'],
        1,
        *buttons_list,
        cancel_button=False,
    )

    await callback.message.answer(
        text=i18n['phrases']['client_update_fill_first_name'],
        reply_markup=keyboard
    )
    await state.set_state(FSMClientUpdate.fill_first_name)


@router.callback_query(
    ~StateFilter(default_state, FSMDefault.default),
    F.data == 'cancel'
)
async def photo_cancel(
    callback: CallbackQuery, state: FSMContext, i18n: dict
):

    await callback.message.answer(
        text=i18n['phrases']['cancel']
    )
    await state.clear()
    await state.set_state(FSMDefault.default)


@router.callback_query(
    StateFilter(FSMStart.start),
    F.data == 'cancel'
)
async def cancel(
    callback: CallbackQuery, i18n: dict
):
    await callback.message.answer(
        text=i18n['phrases']['cancel']
    )
