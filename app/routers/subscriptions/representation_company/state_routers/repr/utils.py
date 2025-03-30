from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.config import settings as st
from core.terminology import Lang as core_Lang, terminology as core_term
from schemas.representations import SubscriptionListSchema
from schemas.utils import FailSchema
from services.subscriptions import get_subscription_service
from routers.default.state import FSMDefault


async def calc_offset(page: int, total_count: int):
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
    company_uuid: str,
    lang: str,
    message: Message,
    state: FSMContext,
    total_count: int = None,
    page: int = 1,
):
    if page != 1 and total_count is None:
        raise Exception()
    service = get_subscription_service()
    if page == 1:
        offset = 0
    else:
        offset, page = await calc_offset(page=page, total_count=total_count)
    data: SubscriptionListSchema = await service.get_list(
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
        result.append(
            {
                'num': count,
                'uuid': item.uuid,
                'name': f'{item.client.first_name} {item.client.last_name}'
            }
        )

    return result, page
