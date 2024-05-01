from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnSch = KeyboardButton('Узнать расписание')
btnGroup = KeyboardButton('Изменить группу')
btnGroupName = KeyboardButton('Узнать группу')
btnNotif = KeyboardButton('Уведомления')

btnBack = KeyboardButton('Назад')
btnNotifOn = KeyboardButton('Включить')
btnNotifOff = KeyboardButton('Выключить')

notifon = ReplyKeyboardMarkup().add(btnNotifOn, btnBack)
notifoff = ReplyKeyboardMarkup().add(btnNotifOff, btnBack)
mainMenu = ReplyKeyboardMarkup().add(btnSch, btnGroupName, btnGroup, btnNotif)

btnToday = KeyboardButton('Расписание на сегодня')
btnNextday = KeyboardButton('Расписание на завтра')
btnWeek = KeyboardButton('Расписание на ближайшие 7 дней')
btnNextweek = KeyboardButton('Расписание на следующую неделю')
btnMain = KeyboardButton('Главное меню')
btnAllSch = KeyboardButton('Всё рапсисание')

dayMenu = ReplyKeyboardMarkup().row(btnToday, btnNextday).row(btnWeek, btnAllSch).add(btnMain)

btnOdd = KeyboardButton('Нечетная неделя')
btnEven = KeyboardButton('Четная неделя')

weekMenu = ReplyKeyboardMarkup().row(btnOdd, btnEven).add(btnMain)