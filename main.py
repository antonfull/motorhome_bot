from aiogram import Bot, Dispatcher, F
import asyncio
from dotenv import load_dotenv
import os
from utils.commands import set_commands
from handlers.register import start_register,register_name, register_phone
from handlers.start import get_start
from aiogram.filters import Command
from handlers.user_game import viewn_user_game
from handlers.profile import viewn_game, viewn_game_date, add_match_player, delete_match_player
from state.register import RegisterState
from state.create import CreateState
from filters.CheckAdmin import CheckAdmin
from handlers.admin.create import create_game, select_place, select_date, select_time, select_minplayer, select_maxplayer, select_price

load_dotenv()

#Объявление переменных окружения
token = os.getenv('TOKEN')
admin_id = os.getenv('ADMIN_ID')

bot = Bot(token=token)
dp = Dispatcher()

#Уведомление админа, что бот запущен
async def start_bot(bot: Bot):
    await bot.send_message(732737012, text='Я запустил бота')

dp.startup.register(start_bot)

#Регистрируем кнопку старт
dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))

#Регистрируем кнопку регистрации
dp.message.register(start_register, F.text == 'Зарегистрироваться на сайте')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_phone, RegisterState.regPhone)

#Регистрируем хендлер для создания тура
dp.message.register(create_game, Command(commands='create'), CheckAdmin())
dp.callback_query.register(select_place, CreateState.place)
dp.callback_query.register(select_date, CreateState.date)
dp.callback_query.register(select_time, CreateState.time)
dp.message.register(select_minplayer, CreateState.motorvehicle)
dp.message.register(select_maxplayer, CreateState.maxPlayer)
dp.message.register(select_price, CreateState.price)
#Просмотр профиля и его изменения
dp.message.register(viewn_game, F.text == 'Актуальные туры')
dp.callback_query.register(viewn_game_date, F.data.startswith('viewn_date_'))
dp.callback_query.register(add_match_player, F.data.startswith('add_match'))
dp.callback_query.register(delete_match_player, F.data.startswith('delete_match'))
dp.message.register(viewn_user_game, F.text == 'Мои туры')

#Пробуем запускать бота, если неудача, то закрываем его
async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())