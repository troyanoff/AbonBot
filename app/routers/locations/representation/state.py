from aiogram.fsm.state import State, StatesGroup


class FSMLocationRepr(StatesGroup):
    repr = State()
    core_buttons = ('back_state', )


states_group = FSMLocationRepr
