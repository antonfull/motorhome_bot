from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
import re
import os
from utils.database import Database

#Функция начала регистрации
async def start_register(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if(users):
        await bot.send_message(message.from_user.id, f'{users[1]} \n Вы уже зарегистрированы')
    else:
        await bot.send_message(message.from_user.id,f'Давайте начнем регистрацию \n Для начала скажите, как к Вам обращаться?')
        await state.set_state(RegisterState.regName)

#Функция обработки имени пользователя
async def register_name(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id,f'Приятно познакомиться {message.text} \n'
                         f'Теперь укажите номер телефона \n'
                         f'Формат телефона: +7--------- \n\n\n')
    #Сохраняем имя по ключу в хранилище
    await  state.update_data(regname=message.text)
    await  state.set_state(RegisterState.regPhone)

#Функция обработки номера телефона
async def register_phone(message: Message, state: FSMContext, bot: Bot):
    if(re.findall('^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message.text)):
        await state.update_data(regphone=message.text)
        reg_data = await state.get_data()
        reg_name = reg_data.get('regname')
        reg_phone = reg_data.get('regphone')
        msg = f'Приятно познакомиться {reg_name} \n\n Телефон - {reg_phone}'
        await bot.send_message(message.from_user.id, msg)
        db = Database(os.getenv('DATABASE_NAME'))
        db.add_user(reg_name, reg_phone, message.from_user.id)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id,f'Номер указан в неправильном формате')