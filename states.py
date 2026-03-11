from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    name = State()
    surname = State()
    age = State()
    phone = State()
    tasdiqlash = State()
    