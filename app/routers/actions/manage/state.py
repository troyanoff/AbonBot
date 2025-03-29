from aiogram.fsm.state import State, StatesGroup


class FSMActionManage(StatesGroup):
    manage = State()
    core_buttons = ('back_state', )


states_group = FSMActionManage
