from aiogram.fsm.state import StatesGroup, State

class CreateState(StatesGroup):
    place = State()
    date = State()
    time = State()
    motorvehicle = State()
    maxPlayer = State()
    price = State()