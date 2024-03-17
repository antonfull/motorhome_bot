from aiogram import Bot
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
from utils.database import Database
import os
from keyboards.profile_kb import profile_kb

#Обрабатываем нажатия на кнопки
async def get_start(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'Здравствуйте, {users[1]}!', reply_markup=profile_kb())
    else:
        await bot.send_message(message.from_user.id, f'Здравствуйте, рад видеть Вас! \n'
                                                 f'Бот поможет вам забранировать автодом 🚐, расскажет все подробности \n'
                                                 f'Также вы сможете отслеживать статистику Ваших путешествий ⛰ \n\n\n'
                           , reply_markup=register_keyboard)

