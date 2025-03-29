from aiogram.fsm.state import State, StatesGroup


class FSMLocationUpdate(StatesGroup):
    name = State()
    description = State()
    photo = State()
    photo_callbacks = ('photo_cancel', )
    city = State()
    street = State()
    house = State()
    flat = State()
    timezone = State()
    miss_button = 'miss_state'
    core_buttons = ('miss_state', 'cancel', )


package_state = FSMLocationUpdate
