from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dataclasses import dataclass, field
from pydantic import BaseModel

from core.config import settings as st
from handlers.base import Data, BaseConfig, BaseHandler, LastMessage, RequestTG
from schemas.base import BaseReprListSchema
from services.base import BaseService


@dataclass
class ReprConfig(BaseConfig):
    item_name: list = field(default_factory=lambda: [])
    format_caption: dict = None


class ReprBase(BaseHandler):
    def __init__(
        self,
        config: ReprConfig
    ):
        self.config = config
        self._register_handlers()

    def _register_handlers(self):
        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.regexp((r'^back:\d+:\d+$'))
        )(self.back)

        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.regexp((r'^forward:\d+:\d+$'))
        )(self.forward)

        self.config.router.callback_query(
            StateFilter(self.config.router_state),
            F.data.regexp((
                    r'^'
                    + f'{self.config.item_prefix}'
                    + r':[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab]'
                    + r'[0-9a-f]{3}-[0-9a-f]{12}$'
                ))
        )(self.choice_item)
        super()._register_handlers()

    async def _get_filter(self, data: Data):
        state_data = await data.request.state.get_data()
        return {k: state_data[v] for k, v in self.config.list_filter.items()}

    async def _create_caption(self, data: Data) -> str:
        if not self.config.format_caption:
            return data.term.local.terms.list_items
        state_data = await data.request.state.get_data()
        content = {
            k: state_data[v] for k, v in self.config.format_caption.items()}
        result = data.term.local.terms.list_items.format(**content)
        return result

    async def _choise_media(self, data: Data) -> str:
        return getattr(data.term.core.photos, self.config.stug_photo_name)

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
        data: Data,
        total_count: int = None,
        page: int = 1,
    ):
        if page != 1 and total_count is None:
            raise Exception()
        if page == 1:
            offset = 0
        else:
            offset, page = await self.calc_offset(
                page=page, total_count=total_count)

        service: BaseService = self.config.service_caller()
        filters = await self._get_filter(data)
        items: BaseReprListSchema = await service.get_list(
            **filters, offset=offset)

        if await self.bad_response(data, items):
            return

        result = []
        count = offset
        for item in items.items:
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

    async def pages_inline_kb(
        self,
        data: Data,
        items: list[dict],
        page: int,
        total_count: int
    ) -> InlineKeyboardMarkup:
        kb_builder = InlineKeyboardBuilder()
        kb_buttons: list[InlineKeyboardButton] = []
        for item in items:
            kb_buttons.append(InlineKeyboardButton(
                text=f'{item['num']} {item['name']}',
                callback_data=f'{self.config.item_prefix}:{item['uuid']}'))
        kb_builder.row(*kb_buttons, width=1)
        if total_count > st.default_limit_keyboard_page:
            kb_builder.row(
                InlineKeyboardButton(
                    text=data.term.core.buttons.back,
                    callback_data=f'back:{total_count}:{page}'
                ),
                InlineKeyboardButton(
                    text=data.term.core.buttons.forward,
                    callback_data=f'forward:{total_count}:{page}'
                ),
                width=2
            )

        if self.config.callbacks:
            callbacks = await data.term.local.buttons.get_dict_with(
                *self.config.callbacks
            )
            add_butt = []
            for k, v in callbacks.items():
                add_butt.append(
                    InlineKeyboardButton(
                        text=v,
                        callback_data=k
                    )
                )
            kb_builder.row(*add_butt, width=1)
        back_reason = await self.back_state_group_exist(data)
        if back_reason and self.config.back_button:
            button_data = await data.term.core.buttons.get_dict_with(
                self.config.back_button)
            callback_data, text = list(button_data.items())[0]
            kb_builder.row(
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback_data
                )
            )
        return kb_builder.as_markup()

    async def _create_keyboard(
        self, data: Data, total_count: int = None, page: int = 1
    ) -> InlineKeyboardMarkup:
        if not total_count:
            keyboard = await self.create_simply_kb(data)
            return keyboard
        data_pages, page = await self.create_page(data, total_count, page)
        keyboard = await self.pages_inline_kb(
            data=data,
            items=data_pages,
            page=page,
            total_count=total_count
        )
        return keyboard

    async def update_for_next_state(self, data: Data, item: BaseModel):
        update_data = {f'{self.config.item_prefix}_uuid': item.uuid, }

        await data.request.state.update_data(
            {f'{self.config.item_prefix}_uuid': item.uuid, }
        )
        if self.config.item_prefix == 'company':
            update_data.update(
                {f'{self.config.item_prefix}_name': item.name, }
            )
        await data.request.state.update_data(update_data)

    async def repr_item_name(self, item: BaseModel) -> str:
        result = []
        for i in self.config.item_name:
            result.append(await self._getattr_model(item, i))
        return ' '.join(result)

    async def not_items(self, data: Data):
        text = data.term.local.terms.not_items
        photo = await self._choise_media(data)
        keyboard = await self._create_keyboard(data)
        state_data = await data.request.state.get_data()
        last_message = LastMessage(
            state=self.config.router_state.state,
            text=text,
            photo=photo,
            keyboard=keyboard,
            state_instance=state_data
        )
        await self.remember_answer(data, last_message)
        await self.answer(data, last_message)

    async def many_items(
        self,
        data: Data,
        items: BaseReprListSchema
    ):
        keyboard = await self._create_keyboard(data, items.total_count, 1)
        text = await self._create_caption(data)
        photo = await self._choise_media(data)
        state_data = await data.request.state.get_data()
        last_message = LastMessage(
            state=self.config.router_state.state,
            text=text,
            photo=photo,
            keyboard=keyboard,
            state_instance=state_data
        )
        await self.remember_answer(data, last_message)
        await self.answer(data, last_message)

    async def one_item(
        self,
        data: Data,
        item: BaseModel
    ):
        await self.update_for_next_state(data, item=item)
        caller = await self.choise_caller(self.config.next_state_caller)
        await caller(data.request)

    async def __call__(
        self,
        request_tg: RequestTG
    ):
        data: Data = self._update_to_request_data('start', request_tg)
        await self.next_state_group(data)

        filters = await self._get_filter(data)
        service: BaseService = self.config.service_caller()
        items: BaseReprListSchema = await service.get_list(**filters)

        if await self.bad_response(data, items):
            return

        if not items.total_count:
            await self.not_items(data)
            return

        if items.total_count == 1:
            await self.one_item(data, items.items[0])
            return

        await self.many_items(data, items)

    async def back(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        data: Data = self._get_request_data(
            'back', callback, lang, state
        )

        split_data = callback.data.split(':')
        total_count = int(split_data[1])
        page = int(split_data[2]) - 1  # back handler

        text = await self._create_caption(data)
        photo = await self._choise_media(data)
        keyboard = await self._create_keyboard(data, total_count, page)
        state_data = await data.request.state.get_data()
        last_message = LastMessage(
            state=self.config.router_state.state,
            text=text,
            photo=photo,
            keyboard=keyboard,
            state_instance=state_data
        )
        await self.remember_answer(data, last_message)
        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard
        )

    async def forward(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        data: Data = self._get_request_data(
            'forward', callback, lang, state
        )

        split_data = callback.data.split(':')
        total_count = int(split_data[1])
        page = int(split_data[2]) + 1  # forward handler

        text = await self._create_caption(data)
        photo = await self._choise_media(data)
        keyboard = await self._create_keyboard(data, total_count, page)
        state_data = await data.request.state.get_data()
        last_message = LastMessage(
            state=self.config.router_state.state,
            text=text,
            photo=photo,
            keyboard=keyboard,
            state_instance=state_data
        )
        await self.remember_answer(data, last_message)
        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard
        )

    async def choice_item(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        data: Data = self._get_request_data(
            'choice_item', callback, lang, state
        )
        uuid = callback.data.split(':')[-1]
        service: BaseService = self.config.service_caller()
        item = await service.get(uuid=uuid)

        if await self.bad_response(data, item):
            return

        await self.one_item(data, item)
