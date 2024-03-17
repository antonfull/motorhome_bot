from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from utils.database import Database
import os
from keyboards.profile_kb import data_kb, add_match, delete_match
from utils.function import list_gamer

async def viewn_game(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Выберите дату тура', reply_markup=data_kb())

async def viewn_game_date(call: CallbackQuery):
    await call.answer()
    date = call.data.split("_")[-1]
    db = Database(os.getenv('DATABASE_NAME'))
    games = db.select_games('0', date)
    if(games):
        await call.message.answer(f'Актуальные игры:')
        for game in games:
            players = db.select_player(game[0])
            gamers = list_gamer(players)
            msg = (f'🧭Тур состоится: {game[9]} (⛰ Адрес: {game[10]}) \n\n'
                   f'🕐{game[2]} в {game[3]} \n\n'
                   f'🚐Автодом: {game[4]} \n\n'
                   f'👨🏻Максимум пассажиров - {game[5]}\n\n'
                   f'💵 Стоимость: {game[6]} \n\n'
                   f'{gamers}')
            if not(db.check_user(game[0], call.from_user.id)):
                await call.message.answer(msg, reply_markup=add_match(game[0], call.from_user.id))
            else:
                await call.message.answer(msg, reply_markup=delete_match(game[0], call.from_user.id))

    else:
        await call.message.answer(f'В выбранную дату не планируется туров')

async def add_match_player(call: CallbackQuery):
    db = Database(os.getenv('DATABASE_NAME'))
    game = db.select_game(0, call.data.split('_')[-2])
    if not (db.check_user(game[0], call.from_user.id)):
        db.add_user_match(game[0], call.from_user.id)
    players = db.select_player(game[0])
    gamers = list_gamer(players)
    msg = (f'🧭Тур состоится: {game[9]} (⛰ Адрес: {game[10]}) \n\n'
           f'🕐{game[2]} в {game[3]} \n\n'
           f'🚐Автодом: {game[4]} \n\n'
           f'👨🏻Максимум пассажиров - {game[5]}\n\n'
           f'💵 Стоимость: {game[6]} \n\n'
           f'{gamers}')
    await  call.message.edit_text(msg, reply_markup=delete_match(game[0], call.from_user.id))

async def delete_match_player(call: CallbackQuery):
    db = Database(os.getenv('DATABASE_NAME'))
    game = db.select_game(0, call.data.split('_')[-2])
    if (db.check_user(game[0], call.from_user.id)):
        db.delete_user_match(game[0], call.from_user.id)
    players = db.select_player(game[0])
    gamers = list_gamer(players)
    msg = (f'🧭Тур состоится: {game[9]} (⛰ Адрес: {game[10]}) \n\n'
           f'🕐{game[2]} в {game[3]} \n\n'
           f'🚐Автодом: {game[4]} \n\n'
           f'👨🏻Максимум пассажиров - {game[5]}\n\n'
           f'💵 Стоимость: {game[6]} \n\n'
           f'{gamers}')

    await call.message.edit_text(msg, reply_markup=add_match(game[0], call.from_user.id))
