import sqlite3
from datetime import datetime
import pickle

base = sqlite3.connect('database/bot.db')
cursor = base.cursor()

def sql_start():
    if base:
        print('База данных подключена!')
    cursor.execute('CREATE TABLE IF NOT EXISTS info (name TEXT, start_date TEXT, end_date TEXT, parsing_permission INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name_group TEXT, notif INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS groups (name_group TEXT, schedule TEXT, request INTEGER)')
    base.commit()


async def add_user(user_id):
    cursor.execute('INSERT INTO users VALUES (?, ?, ?)', (user_id, 'no_group', 0))
    base.commit()

async def add_group(group):
    all_groups = [id_[0] for id_ in await get_all_groups()]
    
    if group not in all_groups:
        cursor.execute('INSERT INTO groups VALUES (?, ?, ?)', (group, 'no_schedule', 0))
        base.commit()
    else:
        return 0
    
async def add_info(name):
    all_info = [id_[0] for id_ in await get_all_info()]
    
    if name not in all_info:
        cursor.execute('INSERT INTO info VALUES (?, ?, ?, ?)', (name, '01.01.2000', '31.12.2100', 0))
        base.commit()
    else:
        return 0
    

async def add_all():
    await add_info('ITMO')
    with open('groups/allgroups.pkl', 'rb') as file:
        allg = pickle.load(file)
    for i in allg:
        await add_group(i)

async def get_all_users():
    return [u for u in cursor.execute('SELECT * FROM users')]

async def get_all_groups():
    return [u for u in cursor.execute('SELECT * FROM groups')]

async def get_all_info():
    return [u for u in cursor.execute('SELECT * FROM info')]

async def get_notif_users():
    return [u for u in cursor.execute('SELECT tg_id FROM users WHERE notif = 1')]

async def change_user_group(user_id, group_name):
    cursor.execute('UPDATE users SET name_group = ? WHERE tg_id = ?', (group_name, user_id))
    base.commit()

async def change_parsing(permission):
    name = "ITMO"
    cursor.execute('UPDATE info SET parsing_permission = ? WHERE name = ?', (permission, name))
    base.commit()

async def change_start_date(date):
    name = "ITMO"
    cursor.execute('UPDATE info SET start_date = ? WHERE name = ?', (date, name))
    base.commit()

async def change_end_date(date):
    name = "ITMO"
    cursor.execute('UPDATE info SET end_date = ? WHERE name = ?', (date, name))
    base.commit()

async def change_notif(user_id, notif):
    cursor.execute('UPDATE users SET notif = ? WHERE tg_id = ?', (notif, user_id))
    base.commit()

async def change_request(group, request):
    cursor.execute('UPDATE groups SET request = ? WHERE name_group = ?', (request, group))
    base.commit()

async def change_schedule(group, schedule):
    cursor.execute('UPDATE groups SET schedule = ? WHERE name_group = ?', (schedule, group))
    base.commit()

async def get_group_name(tg_id):
    cursor.execute('SELECT name_group FROM users WHERE tg_id = ?', (tg_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
    
async def get_notif(tg_id):
    cursor.execute('SELECT notif FROM users WHERE tg_id = ?', (tg_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

async def get_requests(request=1):
    cursor.execute('SELECT name_group FROM groups WHERE request = ?', (request,))
    result = cursor.fetchall()
    if result:
        return [row[0] for row in result]
    else:
        return None

async def get_group_schedule(name_group):
    cursor.execute('SELECT schedule FROM groups WHERE name_group = ?', (name_group,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

async def get_parsing_permition():
    name = "ITMO"
    cursor.execute('SELECT parsing_permission FROM info WHERE name = ?', (name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
    
async def get_start_date():
    name = "ITMO"
    cursor.execute('SELECT start_date FROM info WHERE name = ?', (name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

async def get_end_date():
    name = "ITMO"
    cursor.execute('SELECT end_date FROM info WHERE name = ?', (name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
