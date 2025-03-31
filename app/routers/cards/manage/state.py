from aiogram.fsm.state import State, StatesGroup


class FSMCardManage(StatesGroup):
    manage = State()
    core_buttons = ('back_state', )


states_group = FSMCardManage
