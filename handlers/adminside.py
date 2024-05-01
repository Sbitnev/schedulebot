from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import os
import json
import emoji
from createbot import bot, dp, ADMINS_CHAT_ID
from aiogram import types
from handlers.states import GetGroup, DeleteGroup, UpdateGroup, SetDate
from database import sqldb
from datetime import datetime
from keyb import menukb, inlinekb
from parsersch import parserjson

async def check_date_format(date_string):
    try:
        datetime.strptime(date_string, '%d.%m.%Y')
        return True
    except ValueError:
        return False


# Обработчик команды
@dp.message_handler(commands=['admin'])
async def command_handler(message: types.Message):
    if message.chat.id == ADMINS_CHAT_ID:
        # Ответ на команду только в чате с администратором
        await message.answer("Панель администратора", reply_markup=inlinekb.inline_kb)
    else:
        # Игнорировать команду в других чатах
        pass

@dp.callback_query_handler(text='add_group')
async def add_group_handler(callback: types.CallbackQuery):
    await GetGroup.group.set()
    await bot.send_message(ADMINS_CHAT_ID, "Введите номер группы:", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=GetGroup.group)
async def add_group_handler2(message: types.Message, state: FSMContext):
    number = message.text  
    await state.finish()
    await bot.send_message(ADMINS_CHAT_ID, await parserjson.get_groupschedule(number))

@dp.callback_query_handler(text='delete_group')
async def delete_group_handler(callback: types.CallbackQuery):
    await DeleteGroup.group.set()
    await bot.send_message(ADMINS_CHAT_ID, "Введите номер группы:", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=DeleteGroup.group)
async def delete_group_handler2(message: types.Message, state: FSMContext):
    number = message.text  
    await state.finish()
    await bot.send_message(ADMINS_CHAT_ID, await parserjson.deletegroup(number))

@dp.callback_query_handler(text='update_group')
async def update_group_handler(callback: types.CallbackQuery):
    await UpdateGroup.group.set()
    await bot.send_message(ADMINS_CHAT_ID, "Введите номер группы:", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=UpdateGroup.group)
async def update_group_handler2(message: types.Message, state: FSMContext):
    number = message.text  
    await state.finish()
    await bot.send_message(ADMINS_CHAT_ID, await parserjson.deletegroup(number))
    await bot.send_message(ADMINS_CHAT_ID, await parserjson.get_groupschedule(number))

@dp.callback_query_handler(text='allowparsing')
async def allowparsing(callback: types.CallbackQuery):
    await sqldb.change_parsing(1)
    await bot.send_message(ADMINS_CHAT_ID, "Парсинг для пользователей разрешен", reply_markup=inlinekb.inline_kb)

@dp.callback_query_handler(text='banparsing')
async def banparsing(callback: types.CallbackQuery):
    await sqldb.change_parsing(0)
    await bot.send_message(ADMINS_CHAT_ID, "Парсинг для пользователей запрещен", reply_markup=inlinekb.inline_kb)

@dp.callback_query_handler(text='setdate')
async def set_date(callback: types.CallbackQuery):
    await SetDate.start.set()
    await bot.send_message(ADMINS_CHAT_ID, "Введите дату начала обучения в формате ДД.ММ.ГГГГ:", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=SetDate.start)
async def set_start_date(message: types.Message, state: FSMContext):
    date = message.text
    if not await check_date_format(date):
        await bot.send_message(ADMINS_CHAT_ID, "Неверный формат")
        return
    await SetDate.end.set()
    await sqldb.change_start_date(date)
    await bot.send_message(ADMINS_CHAT_ID, "Введите дату окончания обучения в формате ДД.ММ.ГГГГ:")

@dp.message_handler(state=SetDate.end)
async def set_end_date(message: types.Message, state: FSMContext):
    date = message.text
    start = await sqldb.get_start_date()
    date2 = datetime.strptime(date, '%d.%m.%Y')
    date1 = datetime.strptime(start, '%d.%m.%Y')
    if not await check_date_format(date):
        await bot.send_message(ADMINS_CHAT_ID, "Неверный формат")
        return
    if date1 >= date2:
        await bot.send_message(ADMINS_CHAT_ID, "Дата окончания не может быть раньше даты начала")
        return
    await state.finish()
    await sqldb.change_end_date(date)
    end = await sqldb.get_end_date()
    await bot.send_message(ADMINS_CHAT_ID, f"Время обучения с {start} по {end}", reply_markup=inlinekb.inline_kb)

@dp.callback_query_handler(text='getdate')
async def get_date(callback: types.CallbackQuery):
    start = await sqldb.get_start_date()
    end = await sqldb.get_end_date()
    await bot.send_message(ADMINS_CHAT_ID, f"Время обучения с {start} по {end}", reply_markup=inlinekb.inline_kb)

@dp.callback_query_handler(text='allrequests')
async def all_requests(callback: types.CallbackQuery):
    req = await sqldb.get_requests()
    if req:
        text = ', '.join(req)
        await bot.send_message(ADMINS_CHAT_ID, text, reply_markup=inlinekb.group_kb)
    else:
        await bot.send_message(ADMINS_CHAT_ID, "Нет запросов", reply_markup=inlinekb.inline_kb)

@dp.callback_query_handler(text='admin_menu')
async def admin_menu(callback: types.CallbackQuery):
    await bot.send_message(ADMINS_CHAT_ID, "Панель администратора", reply_markup=inlinekb.inline_kb)

@dp.callback_query_handler(text='add_all_req')
async def add_all_req(callback: types.CallbackQuery):
    req = await sqldb.get_requests()
    for number in req:
        await bot.send_message(ADMINS_CHAT_ID, await parserjson.get_groupschedule(number))
    await bot.send_message(ADMINS_CHAT_ID, "Группы добавлены успешно", reply_markup=inlinekb.inline_kb)

# Обработчик команды
@dp.message_handler(commands=['addall'])
async def command_handler(message: types.Message):
    if message.chat.id == ADMINS_CHAT_ID:
        # Ответ на команду только в чате с администратором
        for i in sqldb.allg:
            await sqldb.add_group(i)
        await message.answer("Успешно")
    else:
        # Игнорировать команду в других чатах
        pass

