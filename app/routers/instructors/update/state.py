from aiogram.fsm.state import State, StatesGroup


class FSMInstrUpdate(StatesGroup):
    photo = State()
    photo_callbacks = ('photo_cancel', )
    core_buttons = ('back_state', )


states_group = FSMInstrUpdate
