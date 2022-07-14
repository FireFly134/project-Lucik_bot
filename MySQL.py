import sqlite3
import button
import telebot
from work import token, token_test, stop_word

from telebot import types

bot = telebot.TeleBot(token);#_test

db = sqlite3.connect('BD/database.db', check_same_thread=False)
sql = db.cursor()

#############################################################
#############      Действия с людьми      ###################
#############################################################
def start(message):
    user_id = message.from_user.id
    sql.execute(f"SELECT ID FROM user WHERE ID = '{user_id}'")
    answer = sql.fetchone()
    if answer is None:
        return 0
    else:
        button.new_button(message, "Вот, держи для упращения жизни")
        return 1

def reg_name(message,j): #Приходит сообщение с данными, j - кол-во персов
    if message.text.lower() != "/help":
        user_id = message.from_user.id # записываем ID с телеги
        name = message.text #после вопроса как звать записываем имя
        if j == 0:#записали нового пользователя
            sql.execute(f"SELECT ID FROM user WHERE ID = {user_id}")
            try:
                db_id = sql.fetchone()[0]
                if message.from_user.id == db_id:
                    sql.execute(f"UPDATE user SET Name0 = '{name}' WHERE ID = {db_id}")
                    db.commit()
            except Exception:
                if sql.fetchone() is None:
                    sql.execute(f"INSERT INTO user VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(user_id, name, "none", "none", "none", "none", 0, 0, 0, 0, 0, 1, 0, 1, 0, 15, 9, 0))
                    db.commit()
        elif message.text.lower() in stop_word:
            button.new_button(message,"А, ну ок... (Отмена!)")
            return
        else:
            sql.execute(f"UPDATE user SET Name{j} = '{name}', Number_Of_Characters = {j+1} WHERE ID = {user_id}")
            db.commit()
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        sql.execute(f"SELECT Name{j} FROM user WHERE ID = {user_id}")
        text = sql.fetchone()[0]
        sms = "Ты герой под ником \"" + text + "\"?"
        bot.send_message(message.from_user.id, sms, reply_markup=keyboard)

def Delete(id):
    sql.execute(f"SELECT ID FROM user WHERE ID = {id}")
    answer = sql.fetchone()
    if answer is None:
        return "Такого человека нет!"
    else:
        sql.execute(f"DELETE FROM user WHERE ID = {id}")
        db.commit()
        return "Удален!"

def Edit_Name(message):
    user_id = message.from_user.id  # записываем ID с телеги
    name = message.text  # после вопроса как звать записываем имя
    sql.execute(f"SELECT ID FROM user WHERE ID = {user_id}")
    db_id = sql.fetchone()[0]
    if message.from_user.id == db_id:
        sql.execute(f"UPDATE user SET Name0 = '{name}' WHERE ID = {db_id}")
        db.commit()
        sql.execute(f"SELECT Name0 FROM user WHERE ID = {user_id}")
        text = sql.fetchone()[0]
        sms = "теперь тебя зовут: \"" + text + "\"!"
        bot.send_message(message.from_user.id, sms)

def subscription(user_id):#Подписки и кол-во персов
    sql.execute(f"SELECT Subscription_Rock, Subscription_Energi, Number_Of_Characters, Subscription_Turnir  FROM user WHERE ID = {user_id}")
    subscription = sql.fetchone()
    return subscription

def Number_Of_Characters(user_id): # узнаем только кол-во персов
    sql.execute(f"SELECT Number_Of_Characters FROM user WHERE ID = {user_id}")
    num = sql.fetchone()[0]
    return num

def search_people(message):#ищем в бд и передаем есть или нет
    user_id = message.from_user.id
    sql.execute(f"SELECT Name0 FROM user WHERE ID = {user_id}")
    if sql.fetchone() is None:
        return False
    else:
        return True

def time_zone(message, tz):  ###Узнаем часовой во сколько происходит смена КЗ
    try:
        user_id = message.from_user.id  # записываем ID с телеги
        if message.text.lower() in stop_word:
            sms = "Отмена"
            button.new_button(message, sms)
            return
        else:
            if message.text.isnumeric():
                if 1 <= int(message.text) <= 24:
                    TimeZone = int(message.text) -3
                    if tz == 2: #КЗ
                        sql.execute(f"UPDATE user SET Time_KZ = '{TimeZone}' WHERE ID = {user_id}")
                        db.commit()
                    else: # энергия
                        sql.execute(f"UPDATE user SET Time_energi = '{TimeZone}' WHERE ID = {user_id}")
                        db.commit()
                    sms = "Время умпешно установлено!\n Если Вы ошиблись или время поменяется, всегда можно изменить и тут.\n\n Для этого нажми ⚙️Настройка профиля⚙️ ---> Поменять время..."
                    button.new_button(message, sms)
                else:
                    bot.send_message(message.from_user.id, "Введи время по москве!")
                    bot.register_next_step_handler(message, time_zone, tz)
            else:
                bot.send_message(message.from_user.id, "Вводи цифрами")
                bot.register_next_step_handler(message, time_zone, tz)
    except Exception as ex:
        bot.send_message(message.from_user.id, "Возникла ошибка!Пожалуйста напиши @Menace134 об этом.")
        bot.send_message(943180118, message.from_user.first_name + " пытался изменить время...ОШИБКА")
        print(message.from_user.first_name + " пытался изменить время...ОШИБКА")

def show (sh,user_id):
    sql.execute(f"SELECT {sh} FROM user WHERE ID = {user_id}")
    answer = sql.fetchall()
    return answer

def show_all_ID(clan):
    sql.execute(f"SELECT ID FROM user WHERE ID_Clan {clan}")
    answer = sql.fetchall()
    return answer

def EditInfo(what,ed,user_id):
    sql.execute(f"UPDATE user SET {what} = '{ed}' WHERE ID = {user_id}")
    db.commit()
#############################################################
#############      Действия с людьми      ###################
#############################################################
#############################################################
#############      Действия с Чатом       ###################
#############################################################
def show_End_ID_Clan (): # Выводим последний ID клана или последнюю запись
    sql.execute(f"SELECT * FROM Chat ORDER BY ID_Clan DESC LIMIT 1")
    answer = sql.fetchone()
    return answer

def SendText(clan):# выводим в ответ текст который отправляется людям
    sql.execute(f"SELECT Text_send FROM Chat WHERE ID_Clan = {clan}")
    answer = sql.fetchall()
    return answer

def EditSendText(ed,clan):# Меняем текст который отправляется людям
    sql.execute(f"UPDATE Chat SET Text_send = '{ed}' WHERE ID_Clan = {clan}")
    db.commit()

def EditLink(ed):#редактируем последнюю сылку для поста
    sql.execute(f"UPDATE Chat SET Link_Now = '{ed}' WHERE ID_Clan = 1")
    db.commit()

def showLink ():# Считываем последнюю сылку для поста
    sql.execute(f"SELECT Link_Now FROM Chat WHERE ID_Clan = 1")
    answer = sql.fetchone()[0]
    return answer

def NewChat(name,Chat_id,adminID): # Вызываем при регистрации нового чата
    ID_Clan = show_End_ID_Clan()[0]
    sql.execute(f"SELECT ID FROM Chat WHERE ID = {Chat_id}")
    answer = sql.fetchone()
    if answer is None:
        print(id)
        #sql.execute(f"INSERT INTO Chat VALUES(?,?,?,?,?,?)",(ID_Clan+1, id, name, 15, "Добиваем камушки", "Null"))
        #db.commit()
        #sql.execute(f"CREATE TABLE IF NOT EXISTS AdminChat{ID_Clan+1} (ID BIGINT)")
        #db.commit()
        #NewAdminChat(ID_Clan+1, adminID)

def NewAdminChat(ID_Clan,adminID): # Для добавления админов к определенному чату
    sql.execute(f"INSERT INTO AdminChat{ID_Clan} VALUES({adminID})")
    db.commit()

def DeleteChat(Chat_id): # Удаляем чат
    sql.execute(f"SELECT ID FROM Chat WHERE ID = {Chat_id}")
    answer = sql.fetchone()
    if answer is None:
        return "Такого чата нет!"
    else:
        sql.execute(f"DELETE FROM Chat WHERE ID = {Chat_id}")
        db.commit()
        return "Чат удален!"

#############################################################
#############      Действия с Чатом       ###################
#############################################################

def commands(command):
    sql.execute(command)
    answer = sql.fetchall()
    return answer
