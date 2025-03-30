from aiogram.fsm.state import State, StatesGroup


class FSMActionUpdate(StatesGroup):
    name = State()
    description = State()
    photo = State()
    photo_callbacks = ('photo_cancel', )
    miss_button = 'miss_state'
    core_buttons = ('miss_state', 'cancel', )


states_group = FSMActionUpdate
