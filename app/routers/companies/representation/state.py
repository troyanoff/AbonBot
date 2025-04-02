
from aiogram.fsm.state import State, StatesGroup


class FSMCompanyRepr(StatesGroup):
    repr = State()
    core_buttons = ('cancel', )


states_group = FSMCompanyRepr
