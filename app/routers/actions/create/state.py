from aiogram.fsm.state import State, StatesGroup


class FSMActionCreate(StatesGroup):
    name = State()
    description = State()
    photo = State()
    photo_callbacks = ('photo_cancel', )
    core_buttons = ('cancel', )


states_group = FSMActionCreate
