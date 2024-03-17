from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from utils.database import Database
import os
from utils.function import list_gamer

async def viewn_user_game(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    games = db.user_game(0, message.from_user.id)
    if (games):
        await bot.send_message(message.from_user.id, f'Вы записаны на следующие туры:')
        for game in games:
            players = db.select_player(game[0])
            gamers = list_gamer(players)
            msg = (f'🧭Тур состоится: {game[9]} (⛰ Адрес: {game[10]}) \n\n'
                   f'🕐{game[4]} в {game[5]} \n\n'
                   f'💵 Стоимость: {game[6]} \n\n'
                   f'{gamers}')
            await bot.send_message(message.from_user.id, msg)

    else:
        await bot.send_message(message.from_user.id,f'Вы не записаны на туры')