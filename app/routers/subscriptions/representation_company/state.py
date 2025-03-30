from aiogram.fsm.state import State, StatesGroup


class FSMSubCompanyRepr(StatesGroup):
    repr = State()
    core_buttons = ('back_state', )


states_group = FSMSubCompanyRepr
