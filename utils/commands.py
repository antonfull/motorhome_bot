from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

# Создаем команду запуска бота
async def set_commands(bot: Bot):
    commands = [
        # Это кнопки
        BotCommand(
            command='start',
            description= 'Запускаем Бота'
        ),
        BotCommand(
            command='help',
            description='Помощь в работе с Ботом'
        )
    ]

    await  bot.set_my_commands(commands, BotCommandScopeDefault())