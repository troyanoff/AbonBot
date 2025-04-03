
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, Message, InputMediaPhoto, InlineKeyboardMarkup
)
from dataclasses import dataclass, field
from importlib import import_module
from logging import Logger
from pydantic import BaseModel
from types import CoroutineType

from core.config import settings as st
from core.terminology import terminology as core_term, Lang as core_Lang
from handlers.base import RequestTG, Term
from keyboards.inline.base import create_simply_inline_kb, pages_inline_kb
from schemas.base import BaseReprListSchema
from services.base import BaseService
from utils.support import bad_response
from utils.terminology import LangListBase, LangBase


@dataclass
class ReprConfig:
    logger: Logger
    router: Router
    states_group: StatesGroup
    router_state: State
    service_caller: CoroutineType
    next_state_caller: str
    term: LangListBase
    item_prefix: str
    item_name: list[str]
    back_state_caller: CoroutineType = None
    back_item_uuid_key: str = None
    stug_photo_name: str = 'default'
    list_filter: dict = field(default_factory=lambda: {
        'company_uuid': 'company_uuid'
    })
    callbacks: dict = field(default_factory=lambda: {
        # 'callback_name': 'path to caller'
    })
    format: dict = None


class ReprBase:
    request: RequestTG = None

    def __init__(
        self,
        config: ReprConfig
    ):
        self.config = config
        self._register_handlers()

    def _register_handlers(self):
        if self.config.back_state_caller:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data.in_(('back_state', 'cancel'))
            )(self.cancel)

        if self.config.callbacks:
            self.config.router.callback_query(
                StateFilter(self.config.router_state),
                F.data.in_(self.config.callbacks)
            )(self.callback_caller)

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

    async def _get_filter(self):
        data = await self.request.state.get_data()
        return {k: data[v] for k, v in self.config.list_filter.items()}

    def _register_request(
        self,
        handler_name: str,
        update: CallbackQuery | Message,
        lang: str,
        state: FSMContext
    ):
        state_handler = f'{self.config.router_state.state}:{handler_name}'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
        self.request = RequestTG(update=update, lang=lang, state=state)
        terminology_lang: LangBase = getattr(self.config.term, lang)
        core_term_lang: core_Lang = getattr(core_term, lang)
        self.term = Term(core=core_term_lang, local=terminology_lang)

    async def create_caption(self):
        lang = self.request.lang
        terminology_lang: LangBase = getattr(self.config.term, lang)
        if not self.config.format:
            return terminology_lang.terms.list_items
        print(self.config)
        data = await self.request.state.get_data()
        content = {k: data[v] for k, v in self.config.format.items()}
        result = terminology_lang.terms.list_items.format(**content)
        return result

    async def choise_message(self):
        if isinstance(self.request.update, CallbackQuery):
            return self.request.update.message
        return self.request.update

    async def choise_media(self, item: BaseModel) -> str:
        if getattr(item, 'photo_id', None):
            return item.photo_id
        return getattr(self.term.core.photos, self.config.stug_photo_name)

    async def update_for_next_state(self, item: BaseModel):
        data = {f'{self.config.item_prefix}_uuid': item.uuid, }

        await self.request.state.update_data(
            {f'{self.config.item_prefix}_uuid': item.uuid, }
        )
        if self.config.item_prefix == 'company':
            data.update(
                {f'{self.config.item_prefix}_name': item.name, }
            )
        await self.request.state.update_data(data)

    async def repr_item_name(self, item: BaseModel) -> str:
        result = []
        for i in self.config.item_name:
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
        filters = await self._get_filter()
        items: BaseReprListSchema = await service.get_list(
            **filters, offset=offset)

        # if await bad_response(items, **self.request.__dict__):
        #     return

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

    async def not_items(self):
        lang = self.request.lang
        core_term_lang: core_Lang = getattr(core_term, lang)
        terminology_lang: LangBase = getattr(self.config.term, lang)
        buttons = terminology_lang.buttons.__dict__
        core_buttons = await core_term_lang.buttons.get_dict_with(
            *self.config.states_group.core_buttons)
        buttons.update(core_buttons)

        keyboard = await create_simply_inline_kb(
            buttons,
            1
        )
        if isinstance(self.request.update, CallbackQuery):
            msg = self.request.update.message
        else:
            msg = self.request.update
        await msg.edit_media(
            media=InputMediaPhoto(
                media=getattr(
                    core_term_lang.photos, self.config.stug_photo_name),
                caption=terminology_lang.terms.not_items
            ),
            reply_markup=keyboard
        )
        return

    async def many_items(
        self,
        items: BaseReprListSchema
    ):
        lang = self.request.lang
        core_term_lang: core_Lang = getattr(core_term, lang)
        terminology_lang: LangBase = getattr(self.config.term, lang)
        data_pages, page = await self.create_page()
        keyboard = await pages_inline_kb(
            data=data_pages,
            callback_prefix=self.config.item_prefix,
            page=page,
            total_count=items.total_count,
            lang=lang,
            additional_buttons=terminology_lang.buttons.__dict__,
            back_state=bool(self.config.back_state_caller)
        )
        text = await self.create_caption()
        media = getattr(core_term_lang.photos, self.config.stug_photo_name)
        msg = await self.choise_message()

        if msg.photo:
            await msg.edit_media(
                media=InputMediaPhoto(
                    media=media,
                    caption=text
                ),
                reply_markup=keyboard
            )
        else:
            await msg.answer_photo(
                photo=media,
                caption=text,
                reply_markup=keyboard
            )

    async def one_item(
        self,
        item: BaseModel
    ):
        await self.update_for_next_state(item=item)
        module_path, caller = self.config.next_state_caller.rsplit('.', 1)
        module = import_module(module_path)
        await getattr(module, caller)(**self.request.__dict__)

    async def __call__(
        self,
        update: CallbackQuery | Message,
        lang: str,
        state: FSMContext
    ):
        self.request = RequestTG(update=update, lang=lang, state=state)
        state_handler = f'{self.config.router_state.state}:repr'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')
        await state.set_state(self.config.router_state)

        filters = await self._get_filter()

        service: BaseService = self.config.service_caller()
        items: BaseReprListSchema = await service.get_list(**filters)

        # if await bad_response(items, **self.request.__dict__):
        #     return

        await state.update_data(
            {f'{self.config.item_prefix}_count': items.total_count}
        )

        if not items.total_count:
            await self.not_items()
            return

        if items.total_count == 1:
            await self.one_item(item=items.items[0])
            return

        await self.many_items(items=items)

    async def choise_caller(
        self, caller_entity: str | CoroutineType
    ) -> CoroutineType:
        if isinstance(caller_entity, CoroutineType):
            return caller_entity
        module_path, caller = caller_entity.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, caller)

    async def back_state(self):
        caller = await self.choise_caller(self.config.back_state_caller)
        await caller(**self.request.__dict__)

    async def cancel(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        self.request = RequestTG(update=callback, lang=lang, state=state)
        state_handler = f'{self.config.router_state.state}:back_state'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        await self.back_state()

    async def back(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        self.request = RequestTG(update=callback, lang=lang, state=state)
        state_handler = f'{self.config.router_state.state}:back'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        split_data = callback.data.split(':')
        total_count = int(split_data[1])
        page = int(split_data[2]) - 1  # back handler

        pages_data, page = await self.create_page(
            total_count=total_count,
            page=page,
        )

        terminology_lang: LangBase = getattr(self.config.term, lang)
        keyboard = await pages_inline_kb(
            data=pages_data,
            callback_prefix=self.config.item_prefix,
            page=page,
            total_count=total_count,
            lang=lang,
            additional_buttons=terminology_lang.buttons.__dict__,
            back_state=bool(self.config.back_state_caller)
        )
        text = await self.create_caption()

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
        self.request = RequestTG(update=callback, lang=lang, state=state)
        state_handler = f'{self.config.router_state.state}:forward'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        split_data = callback.data.split(':')
        total_count = int(split_data[1])
        page = int(split_data[2]) + 1  # forward handler

        pages_data, page = await self.create_page(
            total_count=total_count,
            page=page,
        )

        terminology_lang = getattr(self.config.term, lang)
        keyboard = await pages_inline_kb(
            data=pages_data,
            callback_prefix=self.config.item_prefix,
            page=page,
            total_count=total_count,
            lang=lang,
            additional_buttons=terminology_lang.buttons.__dict__,
            back_state=bool(self.config.back_state_caller)
        )
        text = await self.create_caption()

        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard
        )

    async def next_state(self, item: BaseModel):
        await self.update_for_next_state(item=item)
        caller = await self.choise_caller(self.config.next_state_caller)
        await caller(**self.request.__dict__)

    async def choice_item(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        lang: str
    ):
        self.request = RequestTG(update=callback, lang=lang, state=state)
        state_handler = f'{self.config.router_state.state}:to_item'
        self.config.logger.info(f'\n{'=' * 80}\n{state_handler}\n{'=' * 80}')

        uuid = callback.data.split(':')[-1]
        service: BaseService = self.config.service_caller()
        item = await service.get(uuid=uuid)

        if await bad_response(callback.message, state, lang, item):
            return

        await self.next_state(item)

    async def callback_caller(
        self,
        callback: CallbackQuery,
        lang: str,
        state: FSMContext
    ):
        self._register_request(
            handler_name=callback.data,
            update=callback,
            lang=lang,
            state=state
        )
        caller = await self.choise_caller(self.config.callbacks[callback.data])
        await caller(**self.request.__dict__)
