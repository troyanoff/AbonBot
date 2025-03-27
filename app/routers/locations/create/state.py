from aiogram.fsm.state import State, StatesGroup


class FSMLocationCreate(StatesGroup):
    name = State()
    description = State()
    photo = State()
    photo_callbacks = ('photo_cancel', )
    city = State()
    street = State()
    house = State()
    flat = State()
    timezone = State()
    core_buttons = ('cancel', )
