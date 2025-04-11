from aiogram.fsm.state import State, StatesGroup


class FSMInstrRepr(StatesGroup):
    repr = State()
    back_button = 'back_state'


states_group = FSMInstrRepr
