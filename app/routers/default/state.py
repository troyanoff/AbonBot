from aiogram.fsm.state import State, StatesGroup


class FSMDefault(StatesGroup):
    default = State()
    core_buttons = ('miss_state', 'cancel', )


class FSMStart(StatesGroup):
    start = State()
