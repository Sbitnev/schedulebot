from aiogram.dispatcher.filters.state import State, StatesGroup

class ChooseGroup(StatesGroup):
    group = State()

class GetGroup(StatesGroup):
    group = State()

class DeleteGroup(StatesGroup):
    group = State()

class UpdateGroup(StatesGroup):
    group = State()

class SetDate(StatesGroup):
    start = State()
    end = State()

class ChooseNotif(StatesGroup):
    notif = State()