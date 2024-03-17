from aiogram.fsm.state import StatesGroup, State

#Обеспечиваем состояние регистрации
class RegisterState(StatesGroup):
    regName = State()
    regPhone = State()