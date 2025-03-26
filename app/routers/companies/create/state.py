from aiogram.fsm.state import State, StatesGroup


class FSMCompanyCreate(StatesGroup):
    name = State()
    description = State()
    email = State()
    photo = State()
    photo_callbacks = ('photo_cancel', )
    max_hour_cancel = State()
    core_buttons = ('cancel', )
