from aiogram.fsm.state import State, StatesGroup


class FSMLocationManage(StatesGroup):
    manage = State()
    core_buttons = ('back_state', )
