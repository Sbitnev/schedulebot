from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

inline_kb = InlineKeyboardMarkup(row_width=2)
inline_kb.add(
    InlineKeyboardButton(text="Добавить группу", callback_data="add_group"),
    InlineKeyboardButton(text="Удалить группу", callback_data="delete_group"),
    InlineKeyboardButton(text="Обновить группу", callback_data="update_group"),
    InlineKeyboardButton(text="Все запросы", callback_data="allrequests"),
    InlineKeyboardButton(text="Разрешить парсинг", callback_data="allowparsing"),
    InlineKeyboardButton(text="Запретить парсинг", callback_data="banparsing"),
    InlineKeyboardButton(text="Узнать время обучения", callback_data="getdate"),
    InlineKeyboardButton(text="Изменить время обучения", callback_data="setdate")
)
group_kb = InlineKeyboardMarkup(row_width=1)
group_kb.add(
    InlineKeyboardButton(text="Добавить все", callback_data="add_all_req"),
    InlineKeyboardButton(text="Меню", callback_data="admin_menu"),
)