from aiogram.fsm.state import State, StatesGroup


class FSMInstrManage(StatesGroup):
    manage = State()
    core_buttons = ('back_state', )


states_group = FSMInstrManage
