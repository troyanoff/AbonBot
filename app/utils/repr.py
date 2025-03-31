
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, Message, InputMediaPhoto
)
from logging import Logger
from pydantic import BaseModel
from types import CoroutineType

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from keyboards.inline.base import create_simply_inline_kb, pages_inline_kb
from routers.default.state import FSMDefault
from schemas.utils import FailSchema
from utils.support import bad_response


class RerpBase:
    def __init__(
        self,
        logger: Logger,
        router: Router,
        states_group: StatesGroup,
        router_state: State,
        service_caller: CoroutineType,
        manage_caller: CoroutineType,
        back_manage_caller: CoroutineType,
        back_manage_uuid: str,
        back_manage_update_type,
        term,
        callback_prefix: str,
        item_name: list[str],
        stug_photo: str = st.stug_photo
    ):
        self.router = router
        self.logger = logger
        self.states_group = states_group
        self.router_state = router_state
        self.service_caller = service_caller
        self.manage_caller = manage_caller
        self.back_manage_caller = back_manage_caller
        self.back_manage_uuid = back_manage_uuid
        self.back_manage_update_type = back_manage_update_type
        self.term = term
        self.callback_prefix = callback_prefix
        self.item_name = item_name
        self.stug_photo = stug_photo
        self._register_handlers()

    def _register_handlers(self):
        self.router.callback_query(
            StateFilter(self.router_state),
            F.data == 'back_state'
        )(self.back_state)

        self.router.callback_query(
            StateFilter(self.router_state),
            F.data.regexp((r'^back:\d+:\d+$'))
        )(self.back)

        self.router.callback_query(
            StateFilter(self.router_state),
            F.data.regexp((r'^forward:\d+:\d+$'))
        )(self.forward)

        self.router.callback_query(
            StateFilter(self.router_state),
            F.data.regexp((
                    r'^'
                    + f'{self.callback_prefix}'
                    + r':[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab]'
                    + r'[0-9a-f]{3}-[0-9a-f]{12}$'
                ))
        )(self.to_manage)

    async def repr_item_name(self, item: BaseModel) -> str:
        result = []
        for i in self.item_name:
            result.append(getattr(item, i))
        return ' '.join(result)

    async def calc_offset(self, page: int, total_count: int):
        if page == 0:
            remains = total_count % st.default_limit_keyboard_page
            total_pages = total_count // st.default_limit_keyboard_page
            if remains:
                total_pages += 1
            page = total_pages
        offset = (page - 1) * st.default_limit_keyboard_page
        if offset >= total_count:
            return 0, 1  # to top of the list
        return offset, page

    async def create_page(
        self,
        company_uuid: str,
        lang: str,
        message: Message,
        state: FSMContext,
        total_count: int = None,
        page: int = 1,
    ):
        if page != 1 and total_count is None:
            raise Exception()
        service = self.service_caller()
        if page == 1:
            offset = 0
        else:
            offset, page = await self.calc_offset(
                page=page, total_count=total_count)
        data = await service.get_list(
            company_uuid=company_uuid, offset=offset)

        if isinstance(data, FailSchema):
            core_term_lang: core_Lang = getattr(core_term, lang)
            await message.answer(
                text=core_term_lang.terms.error,
                reply_markup=None
            )
            await state.clear()
            await state.set_state(FSMDefault.default)
            return

        result = []
        count = offset
        for item in data.items:
            count += 1
            name = await self.repr_item_name(item)
            result.append(
                {
                    'num': count,
                    'uuid': item.uuid,
                    'name': name
                }
            )

        return result, page

    async def repr(
        self,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext,
    ):
        state_handler = f'{self.router_state.state}:repr'
        self.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
        await state.set_state(self.router_state)

        data = await state.get_data()
        company_uuid = data['company_uuid']

        service = self.service_caller()
        items = await service.get_list(
            company_uuid)

        core_term_lang: core_Lang = getattr(core_term, lang)
        if isinstance(items, FailSchema):
            await callback.message.answer(
                text=core_term_lang.terms.error
            )
            await state.clear()
            await state.set_state(FSMDefault.default)
            return

        terminology_lang = getattr(self.term, lang)
        if not items.total_count:
            buttons = terminology_lang.buttons.__dict__
            core_buttons = await core_term_lang.buttons.get_dict_with(
                *self.states_group.core_buttons)
            buttons.update(core_buttons)

            keyboard = await create_simply_inline_kb(
                buttons,
                1
            )
            await callback.message.answer_photo(
                photo=self.stug_photo,
                caption=terminology_lang.terms.not_items,
                reply_markup=keyboard
            )
            return

        if items.total_count == 1:
            await self.manage_caller(
                message=callback.message, lang=lang, state=state,
                item=items.items[0], edit_text=True
            )
            return

        data_pages, page = await self.create_page(
            company_uuid=company_uuid,
            lang=lang,
            message=callback.message,
            state=state,
        )
        keyboard = await pages_inline_kb(
            data=data_pages,
            callback_prefix=self.callback_prefix,
            page=page,
            total_count=items.total_count,
            lang=lang,
            additional_buttons=terminology_lang.buttons.__dict__
        )

        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=self.stug_photo,
                caption=terminology_lang.terms.list_items.format(
                    company_name=data['company_name']
                )
            ),
            reply_markup=keyboard
        )

    async def back_state(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        state_handler = f'{self.router_state.state}:back_state'
        self.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        data = await state.get_data()
        back_uuid = data[self.back_manage_uuid]
        update = dict(callback=callback)
        if self.back_manage_update_type == Message:
            update = dict(message=callback.message)
        await self.back_manage_caller(
            **update, state=state, lang=lang,
            uuid=back_uuid,
            edit_text=True
        )

    async def back(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        state_handler = f'{self.router_state.state}:back'
        self.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        split_data = callback.data.split(':')
        total_count = int(split_data[1])
        page = int(split_data[2]) - 1  # back handler

        data = await state.get_data()
        company_uuid = data['company_uuid']

        pages_data, page = await self.create_page(
            company_uuid=company_uuid,
            total_count=total_count,
            page=page,
            lang=lang,
            message=callback.message,
            state=state,
        )

        terminology_lang = getattr(self.term, lang)
        keyboard = await pages_inline_kb(
            data=pages_data,
            callback_prefix=self.callback_prefix,
            page=page,
            total_count=total_count,
            lang=lang,
            additional_buttons=terminology_lang.buttons.__dict__,
        )

        await callback.message.edit_caption(
            caption=terminology_lang.terms.list_items.format(
                company_name=data['company_name']
            ),
            reply_markup=keyboard
        )

    async def forward(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        state_handler = f'{self.router_state.state}:forward'
        self.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        split_data = callback.data.split(':')
        total_count = int(split_data[1])
        page = int(split_data[2]) + 1  # forward handler

        data = await state.get_data()
        company_uuid = data['company_uuid']

        pages_data, page = await self.create_page(
            company_uuid=company_uuid,
            total_count=total_count,
            page=page,
            lang=lang,
            message=callback.message,
            state=state,
        )

        terminology_lang = getattr(self.term, lang)
        keyboard = await pages_inline_kb(
            data=pages_data,
            callback_prefix=self.callback_prefix,
            page=page,
            total_count=total_count,
            lang=lang,
            additional_buttons=terminology_lang.buttons.__dict__,
        )

        await callback.message.edit_caption(
            caption=terminology_lang.terms.list_items.format(
                company_name=data['company_name']
            ),
            reply_markup=keyboard
        )

    async def to_manage(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        state_handler = f'{self.router_state.state}:to_manage'
        self.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        uuid = callback.data.split(':')[-1]
        service = self.service_caller()
        item = await service.get(uuid=uuid)

        if await bad_response(callback.message, state, lang, item):
            return

        await self.manage_caller(
            message=callback.message, lang=lang,
            state=state, item=item, edit_text=True
        )
