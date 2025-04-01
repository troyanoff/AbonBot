from aiogram.fsm.state import State, StatesGroup


class FSMCardCreate(StatesGroup):
    name = State()
    description = State()
    by_delta = State()
    delta_callbacks = ('yes', 'no', )
    month_delta = State()
    by_count = State()
    count_callbacks = ('yes', 'no', )
    count = State()
    by_limit = State()
    limit_callbacks = ('yes', 'no', )
    time_limit = State()
    freeze = State()
    freeze_callbacks = ('yes', 'no', )
    freezing_days = State()
    location = State()
    actions = State()
    core_buttons = ('cancel', )
    data_field = 'new_card'


states_group = FSMCardCreate
