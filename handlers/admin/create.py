from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from state.create import CreateState
from keyboards.create_kb import place_kb, data_kb, time_kb
from utils.database import Database
import os

#Выбор тура
async def create_game(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Выберите место тура', reply_markup=place_kb())
    await state.set_state(CreateState.place)

#Выбор места
async def select_place(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Место тура выбрано! \n'
                              f'Дальше выберите дату', reply_markup=data_kb())
    await state.update_data(place=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await state.set_state(CreateState.date)

async def select_date(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Я успешно сохранил дату тура \n'
                              f'Выберите время начала тура', reply_markup=time_kb())
    await state.update_data(date=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await state.set_state(CreateState.time)

async def select_time(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Укажите какой автодом Вы хотите выбрать')
    await state.update_data(time=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(CreateState.motorvehicle)

async def select_minplayer(message: Message, state: FSMContext, bot:Bot):
    if(message.text.isdigit() and 1 <= int(message.text) <= 6):
        await bot.send_message(message.from_user.id, f'Хорошо, теперь укажите число пассажиров, максимум 6')
        await state.update_data(motorvehicle=message.text)
        await state.set_state(CreateState.maxPlayer)
    else:
        await bot.send_message(message.from_user.id, f'Максимальное количество - 6, минимальное - 1')

async def select_maxplayer(message: Message, state: FSMContext, bot:Bot):
    if (message.text.isdigit() and 1 <= int(message.text) <= 6):
        await bot.send_message(message.from_user.id, f'Теперь укажите стоимость тура')
        await state.update_data(maxPlayer=message.text)
        await state.set_state(CreateState.price)
    else:
        await bot.send_message(message.from_user.id, f'Я жду стоимость больше 2000 р.')

async def select_price(message: Message, state: FSMContext, bot:Bot):
    await bot.send_message(message.from_user.id, f'Отлично, я создал тур')
    await state.update_data(price = message.text)
    create_data = await state.get_data()
    create_time = create_data.get('time').split('_')[1]
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_game(create_data['place'], create_data['date'], create_time, create_data['motorvehicle'], create_data['maxPlayer'], create_data['price'])
    await state.clear()