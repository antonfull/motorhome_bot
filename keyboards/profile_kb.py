from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import datetime
#Создаем кнопки актуальных и наших туров
def profile_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text='Актуальные туры')
    kb.button(text='Мои туры')
    kb.adjust(2)
    return kb.as_markup(relize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите действие')

def data_kb():
    kb = InlineKeyboardBuilder()
    current_date = datetime.date.today()
    for i in range(7):
        current_date += datetime.timedelta(days=1)
        kb.button(text=f'{current_date.strftime('%d.%m')}', callback_data=f'viewn_date_{current_date.strftime('%d.%m.%y')}')
    kb.adjust(1)
    return kb.as_markup()

def add_match(game_id, user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Записаться на тур ✅', callback_data=f'add_match_{game_id}_{user_id}')
    kb.adjust(1)
    return kb.as_markup()

def delete_match(game_id, user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Удалить запись ❌', callback_data=f'delete_match_{game_id}_{user_id}')
    kb.adjust(1)
    return kb.as_markup()