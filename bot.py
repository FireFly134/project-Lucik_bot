#!/usr/bin/python
# -*- coding: utf8 -*-
#
#В этой части мы подключаемся к нашему боту
#
import telebot
import datetime
import time
import openpyxl
import buttons, chatterbox, MySQL
from random import randint

import requests

from bs4 import BeautifulSoup

from threading import Thread

from telebot import types

from work import token, token_test, KZ, Chat, stop_word, letter, admins

### Вытаскиваем токен
bot = telebot.TeleBot(token);#_test


#####################################################################################
#######################        Функции         ######################################
#####################################################################################
def zero(spisokIZero): ### Обнуление камней у всех
    try:
        for id in spisokIZero:
            subscription = MySQL.subscription(id)
            j = subscription[2]
            for k in range(j):
                MySQL.EditInfo("Rock"+str(k),0,id)
        print("Смена КЗ, обнуление камней!")
    except Exception:
        print("Опять ошибка на ZERO")

def cheek_rock(spisokI): ###Оповещения про недостаток камней
     try:
        for id in spisokI:
            print("id = " +str(id))
            q=0
            name_pers = ("")
            subscription = MySQL.subscription(id)
            print("subscription = " + str(subscription))
            if subscription[1] == 1:
                j = subscription[2]
                for k in range(j):
                    print(MySQL.show("Rock"+str(k),id)[0][0])
                    if int(MySQL.show("Rock"+str(k),id)[0][0]) < 600:
                        if name_pers == "":
                            name_pers += MySQL.show("Name"+str(k),id)[0][0]
                            q=1
                        else:
                            name_pers += ", " + MySQL.show("Name"+str(k),id)[0][0]
                            q=2
                try:
                    if q == 1:
                        bot.send_message(id, "У героя " + name_pers + " не хватает камней.")
                    elif q == 2:
                        bot.send_message(id, "У героев " + name_pers + " не хватает камней.")
                except:
                    name = MySQL.show("Name0", str(id))
                    bot.send_message(943180118,name + " sms не получил")
                    print(name + " sms оповещение не получил")
     except Exception:
         print("Опять ошибка на Cheek_rock")
def cheek_energi(spisokIEnergi): ###Оповещения про недостаток энергии
    try:
        for id in spisokIEnergi:
            subscription = MySQL.subscription(id)
            if subscription[1] == 1:
                try:
                        bot.send_message(id, "Зайди в игру забери халявную энергию!")
                except:
                    name = MySQL.show("Name0",str(id))
                    bot.send_message(943180118,name + " sms не получил")
                    print(name + " sms оповещение не получил")
    except Exception:
        print("Опять ошибка на Cheek_energi")

def cheek_Turnir(spisokTurnir):
    try:
        for id in spisokTurnir:
            subscription = MySQL.subscription(id)
            if subscription[3] == 1:
                try:
                        bot.send_message(id, "Зайди в игру турнир!")
                except:
                    name = MySQL.show("Name0",str(id))
                    bot.send_message(943180118,name + " sms не получил")
                    print(name + " sms оповещение не получил")
    except Exception:
        print("Опять ошибка на Cheek_Turnir")

def post():
        link = "https://vk.com/ageofmagicgame"

        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
        }

        sait = requests.get(link, headers=header).text

        soup = BeautifulSoup(sait, "lxml")

        post_link = soup.find("a",class_="post_link").get('href')

        if MySQL.showLink() != post_link:
            MySQL.EditLink(post_link)

            text_post = soup.find("div",class_="wall_text")

            sms = str(sms_post(text_post))
            link_img_post = text_post.find_all("a")
            i=len(link_img_post)-1
            N =len(link_img_post[i].get('style')) - 2
            link_img = link_img_post[i].get('style')[50:N]
            img = requests.get(link_img, verify = False).content
            with open("img.jpg", "wb") as image:
                image.write(img)
            for i in range(len(Chat)):
                if i != 4 or i != 5:
                    try:
                        photo = open('img.jpg','rb')
                        bot.send_photo(Chat[i], photo,sms+"\n"+"https://vk.com"+post_link)
                    except:
                        try:
                            bot.send_message(Chat[i],sms)
                            photo = open('img.jpg','rb')
                            bot.send_photo(Chat[i], photo,"https://vk.com"+post_link)
                        except:
                            bot.send_message(admins[0][0], "ERROR: Пост новостей для чата с ID = " +str(Chat[i]) + " не пришел!")

def sms_post(text_post):
    q = 0
    sms = ""
    for i in str(text_post):
        if i == "<":
            com = ""
            q = 1
        elif i == '"':
            if com == 'div class=' or com == 'div class="wall_post_text':
                com+= i
                q = 1
            elif com == 'img alt=':
                com = ""
                q = 2
            else:
                com = ""
                q = 1
        elif i == ">":
            if com == 'div class="wall_post_text"':
                q = 2
            elif com == 'br/':
                sms += "\n"
                q = 2
            else:
                com = ""
                q = 1
        elif q == 1:
            com += i
        elif q == 2:
            sms += i
    return sms

def send_all_king(message):### Отправить всем СМС
    if message.from_user.id == admins[0][0]:#_Devil[0]:
        if message.text.lower() in stop_word:
           button.setting_admin_button(message,"А, ну ок... (ничего не отправил!)")
           return
        else:
            sms = message.text
            answer = MySQL.show_all_ID("")
            for i in range(len(answer)):
                try:
                    bot.send_message(answer[i][0], sms)
                except Exception as ex:
                    name = MySQL.show("Name0", answer[i][0])
                    bot.send_message(message.from_user.id,str(name[0][0]) + " sms не получил")
                    print(message.from_user.first_name + " отправил sms и " + name[0][0] + " sms не получил")
        button.setting_admin_button(message,"Все оповещены")

# def send_all(message,tite,sms):### Отправить всем СМС
#     if message.text.lower() in stop_word:
#        button.setting_admin_button(message,"А, ну ок... (ничего не отправил!)")
#        return
#     else:
#         if tite == 0:
#             for ad in range(len(admins)):
#                 if message.from_user.id in admins[ad]:
#                     id_clan = ad+1
#                     sms = message.text
#         else:
#             for ch in range(len(Chat)):
#                 if message.chat.id == Chat[ch]:
#                     id_clan = ch+1
#         all_id = MySQL.show_all_ID(" = " + str(id_clan))
#         print("all_id = " + str(all_id))
#         for id in all_id:
#             if message.from_user.id == id[0]:
#                 pass
#             else:
#                 try:
#                     bot.send_message(id[0], sms)
#                 except Exception as ex:
#                     print("id = " + str(id[0]) )
#                     name = MySQL.show("Name0",id[0])[0][0]
#                     bot.send_message(message.from_user.id, name +" sms не получил")
#                     print(message.from_user.first_name + " отправил sms и " + name + " sms не получил")
#     button.setting_admin_button(message,"Все оповещены")

# def print_rock(id,k):###вывод камней
#     hours = MySQL.show("Time_KZ",id)
#     now = datetime.datetime.now()
#     time1 = datetime.timedelta(days=now.day,hours=now.hour,minutes=now.minute,seconds=now.second)
#     time2 = datetime.timedelta(days=now.day,hours=hours[0][0],minutes=30,seconds=0)
#     time3 = time2 - time1
#     if time3.days == -1:
#         time2 = datetime.timedelta(days=now.day+1,hours=hours[0][0],minutes=30,seconds=0)
#         time3 = time2 - time1
#     info = MySQL.show("Name" + str(k) + ", Rock" + str(k), id)
#     if info[0][1] == 0:
#         sms = "Ты еще не вводил количество своих камней. Введи количество цифрами!"
#     else:
#         sms = "У твоего героя под ником \""+ info[0][0] +"\" - \"" + str(info[0][1]) +"\" камней! Осталось добить "+ str(600 - info[0][1]) + ". До обновления К.З. осталось " + str(time3)
#     bot.send_message(id, sms)
#####################################################################################
#######################        Функции         ######################################
#####################################################################################

##########################################################################################################################
#Ответы на кнопки
##########################################################################################################################
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if "yes" == call.data:###ДА
        bot.delete_message(call.from_user.id, call.message.message_id)
        num = MySQL.Number_Of_Characters(call.from_user.id)
        if num == 1:
            button.new_button(call,"Приятно познакомиться! Обнуление значений будет по москве в 18:30 и сбор первой энергии в 12:00 ")
            bot.send_message(call.from_user.id,"Время смены КЗ (или сбора энергии), всегда можно изменить.\n\n Для этого нажми ⚙️Настройка профиля⚙️ ---> Поменять время...")
            bot.send_message(call.from_user.id,"Также, можно подписаться на напоминание о сборе энергии и камням(если их не достаточно напомню за час).\n\n Для этого нажми ⚙️Настройка профиля⚙️ ---> Подписаться на напоминалку по камням и энергии")
            cheek_new_user(call.from_user.id, 1)
        else:
            button.new_button(call,"Сохранил!")
    elif "no" == call.data:  ###Нет
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Попробуем еще раз!")
        bot.send_message(call.message.chat.id, "Какой у тебя ник в игре?")
        num = MySQL.Number_Of_Characters(call.from_user.id) - 1
        bot.register_next_step_handler(call.message, MySQL.reg_name,num)
    elif "delete" in call.data:###Когда нажимаешь кнопку ужалить. уточнение, точно ли надо удалять?
        k = int(call.data[7:])
        bot.delete_message(call.from_user.id, call.message.message_id)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        key_yes_del = types.InlineKeyboardButton(text='Да', callback_data='Da_del'+str(k))
        keyboard.add(key_yes_del)
        key_no_del = types.InlineKeyboardButton(text='Нет', callback_data='HET_del')
        keyboard.add(key_no_del)
        delName = MySQL.show("Name" + str(k), call.from_user.id)
        question = "Ты хочешь удалить героя под ником \"" + delName[0][0] + "\"?"
        bot.send_message(call.message.chat.id, text = question, reply_markup=keyboard)
    elif "DelPeopleClan" in call.data:
        id = int(call.data[13:])
        bot.delete_message(call.from_user.id, call.message.message_id)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        key_yes_del = types.InlineKeyboardButton(text='Да', callback_data='Da_Clan_del'+str(id))
        keyboard.add(key_yes_del)
        key_no_del = types.InlineKeyboardButton(text='Нет', callback_data='HET_del')
        keyboard.add(key_no_del)
        delName = MySQL.show("Name0", id)
        question = "Ты хочешь выгнать героя под ником \"" + delName[0][0] + "\" из клана?"
        bot.send_message(call.message.chat.id, text = question, reply_markup=keyboard)
    elif "Da_del" in call.data:  ### Да удалить
        k = int(call.data[6:])
        id = call.from_user.id
        delName = MySQL.show("Name"+str(k), id)
        num = MySQL.Number_Of_Characters(id)
        MySQL.EditInfo("Number_Of_Characters", num - 1 ,id)
        bot.delete_message(call.from_user.id, call.message.message_id)
        button.new_button(call,"Герой с ником \""+delName[0][0]+"\" удален!")
        for i in range(num-1-k):
            info = MySQL.show("Name" + str(i+k + 1) + ", Rock" + str(k + 1), id)
            MySQL.EditInfo("Name" + str(i+k), info[0][0], id)
            MySQL.EditInfo("Rock" + str(i+k), info[0][1], id)
        MySQL.EditInfo("Name" + str(i+k+1), "none", id)
        MySQL.EditInfo("Rock" + str(i+k+1), 0, id)
    elif "Da_Clan_del" in call.data:  ### Да удалить
        id = int(call.data[11:])
        delName = MySQL.show("Name0", id)
        bot.delete_message(call.from_user.id, call.message.message_id)
        button.new_button(call,"Герой с ником \""+delName[0][0]+"\" выгнан из клана!")
        MySQL.EditInfo("ID_Clan", 0, id)
    elif "HET_del" == call.data:###Нет, не удалять.
        bot.delete_message(call.from_user.id, call.message.message_id)
        button.new_button(call,"Ну и отлично!)")
    elif "print" in call.data:  ###Ввывод информации про камни если много героев.
        k = int(call.data[5:6])
        bot.delete_message(call.from_user.id, call.message.message_id)
        print_rock(call.from_user.id,k)
    elif "Add_Rock" in call.data:  ### Добавление камней
        k = int(call.data[8:9])
        j=17
        kol_vo = call.message.text[14:j]
        while True:
            if kol_vo.isnumeric():
                break
            j-=1
            kol_vo = call.message.text[14:j]
        bot.delete_message(call.from_user.id, call.message.message_id)
        add_rock(int(kol_vo),k,call.from_user.id)
    elif "send" in call.data:###Отправка сообщения человеку.
        id = int(call.data[4:])
        name = MySQL.show("Name0",id)
        for ad in range(len(admins)):
            if call.from_user.id in admins[ad]:
                text = MySQL.SendText(str(ad+1))
        try:
            bot.send_message(id, text[0])
            bot.send_message(call.from_user.id, name[0][0] + " сообщение получил(a).")
        except Exception:
            bot.send_message(call.from_user.id,name[0][0] + " сообщение НЕ получил(a).")
    elif "YClanY" in call.data:### Да он в клане
        j = 20
        id = call.data[6:j]
        while True:
            if id.isnumeric():
                break
            j -= 1
            id = call.data[6:j]
        ID_Clan = int(call.data[j+1:])
        print("id - " +str(id))
        print("id_clan - " +str(ID_Clan))
        MySQL.EditInfo("ID_Clan",ID_Clan,id)
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Пометил, "+MySQL.show("Name0",id)[0][0]+" в клане!")
    elif "NClanN" in call.data:### Нет он не в клане
        j = 20
        id = call.data[6:j]
        while True:
            if id.isnumeric():
                break
            j -= 1
            id = call.data[6:j]
        ID_Clan = int(call.data[j + 1:])
        print("id - " + str(id))
        print("id_clan - " + str(ID_Clan))
        MySQL.EditInfo("ID_Clan", ID_Clan, id)
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Пометил, " + MySQL.show("Name0", id)[0][0] + " НЕ в клане!")
        cheek_new_user(id,ID_Clan+1)
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
def edit_send(message):
    if message.text.lower() in stop_word:
        button.setting_admin_button(message,"Отмена")
        return
    else:
        button.setting_admin_button(message,"Сохранил")
        for ad in range(len(admins)):
            if message.from_user.id in admins[ad]:
                MySQL.EditSendText(message.text,ad+1)
    ##################################################################
#
# def delete(num,id):
#     keyboard = types.InlineKeyboardMarkup()
#     for k in range(num):
#         name = MySQL.show("Name" + str(k),id)
#         key_del_nik = types.InlineKeyboardButton(text=name[0][0], callback_data='delete'+str(k))
#         keyboard.add(key_del_nik)
#     bot.send_message(id, "Кого будем удалять?" , reply_markup=keyboard)
###
# def add_rock(sms,num,id):### Добавление камней #В списке 0 - ID, 1 - номер персонажа , 2 - цифры для записи
#     try:
#         Rock = MySQL.show("Rock"+str(num), id)
#         if Rock[0][0] == "0" or Rock[0][0] < sms:
#             MySQL.EditInfo("Rock"+str(num), sms,id)
#             rock = 600 - sms
#             bot.send_message(id, "Ок, я внес изменения. Тебе осталось добить " + str(rock))
#         else:
#             bot.send_message(id,"Ты меня не обманешь! В прошлый раз ты писал "+str(MySQL.show("Rock"+str(num), id)[0][0]))
#     except Exception:
#         bot.send_message(id,"Произошла какая-то ошибка. Попробуй снова!")

# def send_chat(message):###Написать в чат от имени бота
#     try:
#         if message.text.lower() in stop_word:
#             sms = "Отмена"
#             button.new_button(message,sms)
#             return
#         else:
#             for ad in range(len(admins)):
#                 if message.from_user.id in admins[ad]:
#                     id = Chat[ad]
#                     bot.send_message(id,message.text)
#                     button.new_button(message,"Отправлено!")
#     except Exception as ex:
#                 print(message.from_user.username + " отправил sms в чат, но произошла ошибка!")
#                 button.new_button(message,"В чат sms не ушло...хз почему, ошибка!")
# def admin_menu4(message):
#     for ad in range(len(admins)):
#         if message.from_user.id in admins[ad]:
#             id_clan = ad+1
#             keyboard = types.InlineKeyboardMarkup()
#             show_all_ID = MySQL.show_all_ID(" = " + str(id_clan))
#             for id in show_all_ID:
#                 info = MySQL.show("Name0, Rock0",id[0])
#                 key_delete = types.InlineKeyboardButton(text= info[0][0] + " - " +str(info[0][1]), callback_data='DelPeopleClan'+str(id[0]))
#                 keyboard.add(key_delete)
#             bot.send_message(message.from_user.id, "Кто не в клане?", reply_markup=keyboard)
#
#Эти функции позволяют отслеживать время
#
def time_loop():
    while True:
        now = datetime.datetime.now()
        if now.minute == 30 or now.minute == 0:
            post()
            time1 = datetime.timedelta(days=now.day,hours=now.hour,minutes=now.minute)
            spisokI = []
            spisokIEnergi = []
            spisokIZero = []
            spisokTurnir = []
            answer = MySQL.show_all_ID('')
            for id in answer:
                    try:
                        info = MySQL.show("Time_KZ, Time_energi",id[0])
                        time6 = datetime.timedelta(days=now.day,hours=info[0][0],minutes=30)
                        time7 = datetime.timedelta(days=now.day,hours=(info[0][0])-1,minutes=30)

                        time8 = datetime.timedelta(days=now.day,hours=info[0][1],minutes=00)
                        time9 = datetime.timedelta(days=now.day,hours=(info[0][1])+6,minutes=00)
                        time10 = datetime.timedelta(days=now.day,hours=(info[0][1])+9,minutes=00)
                        time11 = datetime.timedelta(days=now.day, hours=10, minutes=00)
                        num_weekday = datetime.datetime.today().weekday()
                        if time6 == time1:
                            print("Оповещение КЗ")
                            spisokIZero += [id[0]]
                        elif time7 == time1:
                            print("Оповещение КЗ -1ч")
                            spisokI += [id[0]]
                        elif time8 == time1 or time9 == time1 or time10 == time1:
                            print("Оповещение про сбор энергии")
                            spisokIEnergi += [id[0]]
                        elif num_weekday == 3:
                            if time11 == time1:
                                print("Оповещение турнира")
                                spisokTurnir += [id[0]]
                    except Exception:
                        name = MySQL.show("Name0",id[0])
                        print("Error: "+name+ "У него не указано время смены КЗ.")

            if spisokIZero != []:
                zero(spisokIZero)
            if spisokI != []:
                cheek_rock(spisokI)
            if spisokIEnergi != []:
                cheek_energi(spisokIEnergi)
            if spisokTurnir != []:
                cheek_Turnir(spisokTurnir)
                print("Отправили на напоминалку Turnir " + str(spisokTurnir))

            time5 = datetime.timedelta(days=now.day,hours=KZ[0]-1,minutes=30) # Оповещение про что остался час до смены КЗ.
            time8 = datetime.timedelta(days=now.day,hours=KZ[1]-1,minutes=30) # Оповещение про что остался час до смены КЗ.
            time9 = datetime.timedelta(days=now.day,hours=KZ[4]-1,minutes=30) # Оповещение про что остался час до смены КЗ.

            if time1 == time5:
                bot.send_message(Chat[0],"До смены кланового задания остался час! Если остались хвосты, подтягивай!🤖")
                bot.send_message(Chat[2],"До смены кланового задания остался час! Если остались хвосты, подтягивай!🤖")
                bot.send_message(Chat[3],"До смены кланового задания остался час! Если остались хвосты, подтягивай!🤖")
                print("Оповещение произошло в 17:30 по мск!")

            if time1 == time8:
                bot.send_message(Chat[1],"До смены кланового задания остался час! Если остались хвосты, подтягивай!🤖")
                bot.send_message(Chat[5],"До смены кланового задания остался час! Если остались хвосты, подтягивай!🤖")
                print("Оповещение произошло в 18:30 по мск!")

            if time1 == time9:
                bot.send_message(Chat[4],"До смены кланового задания остался час! Если остались хвосты, подтягивай!🤖")
                print("Оповещение произошло в 16:30 по мск!")
        time.sleep(60)#Уходим подримать на минутку

########################################################################################################################
########################################################################################################################
########################################################################################################################
def cheek_new_user(id,ID_Clan):
    if MySQL.show_End_ID_Clan()[0] >= ID_Clan:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        key_KlanYes = types.InlineKeyboardButton(text='Да', callback_data='YClanY'+str(id)+"#"+str(ID_Clan))
        keyboard.add(key_KlanYes)
        key_KlanNo = types.InlineKeyboardButton(text='Нет', callback_data='NClanN'+str(id)+"#"+str(ID_Clan))
        keyboard.add(key_KlanNo)
        sms = "Новый герой под ником \"" + MySQL.show("Name0",id)[0][0] + "\". Этот герой из нашего клана?"
        try:
            bot.send_message(admins[ID_Clan-1][0], sms, reply_markup=keyboard)###admin_Devil[0]
        except:
            cheek_new_user(id, ID_Clan+1)
    else:
        MySQL.EditInfo("ID_Clan",0,id)
def del_people(message):
    id = message.text
    bot.send_message(message.from_user.id,MySQL.Delete(id))
#########################################################################################################################
###################    Выполнение команд     ###################
########################################################################################################################
@bot.message_handler(commands=['start'])
def start(message):
    reg = MySQL.start(message)
    if reg == 0:
        bot.send_message(message.from_user.id, "Я тебя не помню. Давай знакомиться! Какой у тебя ник в игре?")
        bot.register_next_step_handler(message, MySQL.reg_name, 0)

@bot.message_handler(commands=['edit_name'])
def edit_name(message):
    bot.send_message(message.from_user.id, "На какое имя будем менять?")
    bot.register_next_step_handler(message, MySQL.Edit_Name)

@bot.message_handler(commands=['help'])
def help(message):
    flag = MySQL.search_people(message)
    if flag:
        sms = "Напиши \"Привет\" чтобы проверить свой ник.\n Можешь кидать количество камней (цифрами) и спросить сколько у тебя камней.\nЗагляни в настройки пользователя, там можешь подписаться на напоминания по сбору халявной энергии или на напоминания по камням за час до смены К.З.(или отписаться)\nЕсли у тебя не один профель в игре, можешь добавить его ник и также кидать на него кол-во камней, но можно добавить не больше 5 героев!\nЕсли возникли проблемы с кнопками напиши /start (не помогло напиши мне @Menace134)"
        button.new_button(message,sms)
        for ad in range(len(admins)):
            if message.from_user.id in admins[ad]:#_Devil or message.from_user.id in admin_Hooliganz or message.from_user.id in admin_Dikaia_jut:
                bot.send_message(message.from_user.id,
                             "Для тебя, "+ message.from_user.first_name + ", ещё есть настройки администратора.\n Там ты сможешь:\n - отправить напоминалку игроку\n"+
                                 "- редактировать сообщение напоминалки\n"+
                                "- отправить ВСЕМ сообщение\n"+
                                "- написать в \"флудилку\" от имени бота.\n"+
                                "- убрать игрока из клана☠")
    else:
        bot.send_message(message.from_user.id,"Я тебя не помню. Давай знакомиться! Какой у тебя ник в игре?")
        bot.register_next_step_handler(message, MySQL.reg_name,0)

@bot.message_handler(commands=['show'])
def show(message):
    if message.from_user.id == 943180118:
        id = str(message.from_user.id)
        sms = MySQL.show("Name0, Rock1", id)
        bot.send_message(id, sms[0][1])

@bot.message_handler(commands=['clear'])
def clear_button(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.from_user.id, "Чтобы сново появились кнопки жми /start", reply_markup=markup)
#
#Админка
#
@bot.message_handler(commands=['send']) #Получаем инфу кто в клане и можем нажав на любого скинуть шаблонное смс
def admin_menu(message):
    for ad in range(len(admins)):
        if message.from_user.id in admins[ad]:
            id_clan = ad + 1
            keyboard = types.InlineKeyboardMarkup()
            show_all_ID = MySQL.show_all_ID(" = " + str(id_clan))
            for id in show_all_ID:
                info = MySQL.show("Name0, Rock0",id[0])
                key_send = types.InlineKeyboardButton(text= info[0][0] + " - " +str(info[0][1]), callback_data='send'+str(id[0]))
                keyboard.add(key_send)
            bot.send_message(message.from_user.id, "Все игроки клана:", reply_markup=keyboard)
@bot.message_handler(commands=['send_edit'])# Редактируем шаблон смс для отправки
def admin_menu2(message):
    for ad in range(len(admins)):
        if message.from_user.id in admins[ad]:#_Devil or message.from_user.id in admin_Hooliganz or message.from_user.id in admin_Dikaia_jut:
            button.cancel_button(message,"Что будем отправлять непослушным деткам?")
            bot.register_next_step_handler(message, edit_send)

@bot.message_handler(commands=['send_all'])# Отправить всем из клана СМС
def admin_send_all_king(message):
    button.cancel_button(message,"Ну, погнали, что отправим?")
    bot.register_next_step_handler(message, send_all_king)

@bot.message_handler(commands=['chat'])# Отправить смс в чат от имени бота
def chat_sms(message):
    for ad in range(len(admins)):
        if message.from_user.id in admins[ad]:
           button.cancel_button(message,"Что написать в чате?")
           bot.register_next_step_handler(message, send_chat)
@bot.message_handler(commands=['post'])# принудительное обнуление камней
def command_post(message):
    post()
@bot.message_handler(commands=['zero'])# принудительное обнуление камней
def zero_pres(message):
    if message.from_user.id == 943180118:
        spisokIZero =[]
        answer = MySQL.show_all_ID("")
        for i in range(len(answer)):
            try:
                spisokIZero+=[answer[i][0]]
            except:
                print("ERROR a 'zero_pres'")
        zero(spisokIZero)
        bot.send_message(message.from_user.id, "Обнулил!")

@bot.message_handler(commands=['show_db'])# вывод экселевской таблици с данными из бд
def show_db(message):
    if message.from_user.id == 943180118:
        q=0
        table = "user"
        while True:
            if q != 2:
                ListWB.active = q
                ListSheet = ListWB.active
                all_id = MySQL.commands(f"SELECT ID FROM {table}")
                i=2
                k=0
                for id in all_id:
                    info = MySQL.commands(f"SELECT * FROM {table} WHERE ID = {id[0]}")[0]
                    for text in info:
                        ListSheet[letter[k] + str(i)].value = str(text)
                        k+=1
                    i+=1
                    k=0
                ListWB.save("list.xlsx")
                q += 1
                table = "Chat"
            else:
                break
        files = open('list.xlsx', 'rb')
        bot.send_document(943180118, files)
        files.close()
@bot.message_handler(commands=['del'])# вывод экселевской таблици с данными из бд
def deletePeople(message):
    if message.from_user.id == 943180118:
        bot.register_next_step_handler(message,del_people)
@bot.message_handler(commands=['edit_clan'])# вывод экселевской таблици с данными из бд
def edit_clan(message):
    if message.from_user.id == 943180118:
        bot.send_message(message.from_user.id, "Введи id")
        bot.register_next_step_handler(message,edit_clan1)
def edit_clan1(message):
    if message.from_user.id == 943180118:
        id = message.text
        bot.send_message(message.from_user.id, "Введи id клана")
        bot.register_next_step_handler(message,edit_clan2,id)
def edit_clan2(message,id):
    if message.from_user.id == 943180118:
        MySQL.EditInfo("ID_Clan",message.text,id)
        bot.send_message(message.from_user.id, "готово!")
###########################################################################
###########################################################################
###########################################################################
@bot.message_handler(commands=['manul_kv'])
def manul_kv(message):    #Инструкция по КВ
    with open('help/kv1.txt','r') as file1:
        text1 = file1.read()
    with open('help/kv2.txt','r') as file2:
        text2 = file2.read()
    with open('help/kv.jpg','rb') as img:
        img = img.read()
        file1.close
        file2.close
    bot.send_message(message.chat.id, text1)
    bot.send_photo(message.chat.id, img)
    bot.send_message(message.chat.id, text2)

@bot.message_handler(commands=['clan_tasks'])
def schedule_of_clan_tasks(message): #Расписание клановых заданий
    with open('help/schedule_of_clan_tasks.txt','r') as file:
        text = file.read()
        file.close
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['date_x2'])
def date_x2(message):
    with open('help/X2.txt','r') as file:
        text = file.read()
        file.close
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['manul_ap_kv'])
def manul_aptechkam_kv(message):#Гайд по аптечкам в КВ
    files = open('help/Manual_KV.doc', 'rb')
    bot.send_document(message.chat.id, files)
    files.close()

@bot.message_handler(commands=['heroes_for_events'])
def necessary_heroes_for_events(message):#Необходимые герои для ивентов
    with open('help/ivent.jpg','rb') as img:
        img = img.read()
    bot.send_photo(message.chat.id, img)

@bot.message_handler(commands=['pak_and_counterpak'])
def pak_and_counterpak(message):#таблица паков и контропаков
    with open('help/pak_and_counterpak.jpg','rb') as img:
        img = img.read()
    bot.send_photo(message.chat.id, img)

@bot.message_handler(commands=['useful_links'])
def useful_links(message):#Полезные ссылки
    with open('help/useful_links.txt','r') as file:
        text = file.read()
        file.close
    bot.send_message(message.chat.id, text)
#
#для обычных смертных
#
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if (message.text.isnumeric() and message.chat.type == "private") or ("люцик добавь" in message.text.lower() and (message.chat.type == "supergroup" or message.chat.type == "group")):
        id = message.from_user.id
        if message.chat.type == "supergroup":
            if message.text[13:].isnumeric():
                sms = message.text[13:]
                bot.send_message(message.chat.id, "Глянь в личку...")
            else:
                bot.send_message(message.chat.id, "Ты что, хочешь меня обмануть? Мне нужны цифры! \n(напиши повторно, на пример: \"Люцик добавь 400\")")
                return
        else:
            sms = message.text
        if 0<=int(sms)<=600:
            num = MySQL.Number_Of_Characters(id)
            if num >= 2:
                keyboard = types.InlineKeyboardMarkup()
                for k in range(num):
                    name = MySQL.show("Name"+str(k),id)
                    key_send_nik = types.InlineKeyboardButton(text=name[0][0], callback_data='Add_Rock'+str(k)+str(sms))
                    keyboard.add(key_send_nik)
                bot.send_message(message.from_user.id, "Кому добавим \"" + message.text + "\" камней?", reply_markup=keyboard)
            else:
                add_rock(int(sms), 0, id)#id кол-во персов и число
        else:
            bot.send_message(message.from_user.id, "Ты что, хочешь меня обмануть? Проверь сколько у тебя камней!")
    elif (("Сколько у меня камней?" in message.text) or ("сколько" in message.text.lower()) and message.chat.type == "private"):# or ("люц" in message.text.lower() and ("камн" in message.text.lower() or "сколько" in message.text.lower())  and (message.chat.type == "supergroup" or message.chat.type == "group")):
        id = message.from_user.id
        num = MySQL.Number_Of_Characters(id)
        if num >= 2:
            keyboard = types.InlineKeyboardMarkup()
            for k in range(num):
                name = MySQL.show("Name" + str(k), id)
                key_send_nik = types.InlineKeyboardButton(text=name[0][0], callback_data='print'+str(k)+str(id))
                keyboard.add(key_send_nik)
            bot.send_message(message.from_user.id, "Кто тебя интересует?", reply_markup=keyboard)
        else:
            print_rock(id,0)
    elif ("прив" in message.text.lower() and message.chat.type == "private") or (("люц" in message.text.lower() or "всем" in message.text.lower() or "доброе" in message.text.lower()) and ("прив" in message.text.lower() or "ку" in message.text.lower() or "здаров" in message.text.lower() or "утр" in message.text.lower())  and (message.chat.type == "supergroup" or message.chat.type == "group") and message.chat.id != Chat[4]):
        id = message.from_user.id
        flag = MySQL.search_people(message)
        if flag:
            name = MySQL.show("Name0",id)[0][0]
        else:
            name = message.from_user.first_name
        rand_num = randint(1,5)
        if rand_num == 1:
            bot.reply_to(message, "Привет, " + name + "!")
        elif rand_num == 2:
            bot.reply_to(message, "Привет, " + name + ", как твои дела?.. Хотя, знаешь,не отвечай... и так знаю что хорошо.")
        elif rand_num == 3:
            bot.reply_to(message, "Ку, " + name)
        elif rand_num == 4:
            bot.reply_to(message, "Привет, " + name + ", ты уже набил 600 камней? Если нет, иди и не возвращайся пока не набьешь!")
        elif rand_num == 5:
            bot.reply_to(message, "Ну привет, " + name + ", если не здоровались")
    elif "люц" in message.text.lower() and "рейд" in message.text.lower() and (message.chat.type == "supergroup" or message.chat.type == "group"):
        bot.reply_to(message, "Сейчас!")
        sms = "Рейд открыт заходим согласно купленным билетам!"
        send_all(message,1,sms)
        if "что" in message.text.lower() or "чё" in message.text.lower() or "чо" in message.text.lower() or "че" in message.text.lower():
            rand_num = 4
        else:
            rand_num = randint(1, 3)
        if rand_num == 1:
            bot.send_message(message.chat.id, "Ану быстро в рейд! Кто последний тот ЛОХ!)")
            sticker = open('AnimatedSticker.tgs', 'rb')
            bot.send_sticker(message.chat.id, sticker)
        elif rand_num == 2:
            bot.send_message(message.chat.id, "Рейд открыт заходим согласно купленным билетам")
            sticker = open('sticker.webp', 'rb')
            bot.send_sticker(message.chat.id, sticker)
        elif rand_num == 3:
            bot.send_message(message.chat.id, "Не вижу ваших жопок на рейде!!! БЫСТРО В РЕЙД!")
        elif rand_num == 4:
            bot.send_message(message.chat.id, "Не знаю как, но нужно закрыть рейд на 100%!")
            video = open('video_2021-05-03_21-46-38.mp4', 'rb')
            bot.send_video(message.chat.id, video)
    # elif "открыт" in message.text.lower() and "рейд" in message.text.lower() and (message.chat.type == "supergroup" or message.chat.type == "group"):
    #     bot.reply_to(message, "В атакууууу... =)")
    #     sms = "Рейд открыт заходим согласно купленным билетам!"
    #     send_all(message, 1, sms)
    #     video = open('video_2021-05-03_21-58-18.mp4','rb')
    #     bot.send_video(message.chat.id, video)
    elif "Помощь" in message.text:
        button.helpMy_button(message,"Вот, листай список, выбирай!")
    elif "Полезная информация" == message.text:
        button.help_button(message,"Вот, листай список, выбирай!")
    elif "Отправить напоминалку игроку" in message.text:
        admin_menu(message)
    elif "Отправить ВСЕМ сообщение" in message.text:
        for ad in range(len(admins)):
            if message.from_user.id in admins[ad]:
                button.cancel_button(message,"Ну, погнали, что отправим?")
                bot.register_next_step_handler(message, send_all,0,None)
    elif "Редактировать сообщение напоминалки" in message.text:
        admin_menu2(message)
    elif "убрать кнопки" in message.text.lower():
        clear_button(message)
    elif "Добавить еще одного героя" in message.text:
        i = MySQL.Number_Of_Characters(message.from_user.id)
        if i <= 4:
            button.cancel_button(message,"Какой у тебя ник в игре?")
            bot.register_next_step_handler(message, MySQL.reg_name,i)
        else:
            bot.send_message(message.from_user.id,"Лимит добавления персонажей привышен!")
    elif "Удалить одного героя" in message.text:
        id = message.from_user.id
        num = MySQL.Number_Of_Characters(id)
        if num >= 2:
            delete(num,id)
        else:
            bot.send_message(message.from_user.id,"У тебя остался только 1 герой!")
    elif "Переименовать героя" in message.text:
        # id = message.from_user.id
        # num = MySQL.Number_Of_Characters(id)
        # if num >= 2:
        #     delete(num,id)
        # else:
            bot.send_message(message.from_user.id,"Пока что функция не доступна!")
    elif "Написать от имени бота🤖" == message.text:
        chat_sms(message)
    elif "Подписаться на напоминалку по камням" == message.text:
        MySQL.EditInfo("Subscription_Rock",1,message.from_user.id)
        button.setting_button(message,"Если у вас будет меньше 600 камней, я вам напобню об этом за час до смены КЗ.")
    elif "Отписаться от напоминалки по камням" == message.text:
        MySQL.EditInfo("Subscription_Rock",0,message.from_user.id)
        button.setting_button(message,"Хорошо, больше не буду вам напоминать про камни... Автоматически.")
    elif "Подписаться на напоминалку по сбору энергии" == message.text:
        MySQL.EditInfo("Subscription_Energi",1,message.from_user.id)
        button.setting_button(message,"Теперь я буду напоминать Вам про энергию.")
    elif "Отписаться от напоминалки по сбору энергии" == message.text:
        MySQL.EditInfo("Subscription_Energi",0,message.from_user.id)
        button.setting_button(message,"Хорошо, больше не буду вам напоминать про энергию...")
    elif "⚙️Настройка профиля⚙️" == message.text:
        button.setting_button(message,"Что будем изменять?")
    elif "🔙Назад🔙" == message.text:
        button.new_button(message,"Погнали, назад, в главное меню.")
    elif "Настройки Админа" == message.text:
        for ad in range(len(admins)):
            if message.from_user.id in admins[ad]:
                button.setting_admin_button(message,"Для тебя, "+ message.from_user.first_name + ", ещё есть такие команды")
    elif "Убрать игрока из клана☠" == message.text:
        for ad in range(len(admins)):
            if message.from_user.id in admins[ad]:
                admin_menu4(message)
    elif "Проверить данные профиля" == message.text:
        ID_Clan = MySQL.show("ID_Clan",message.from_user.id)[0][0]
        print(ID_Clan)
        if ID_Clan == 1:
            clan='Ты в клане "Dev1l"'
        elif ID_Clan == 2:
            clan = 'Ты в клане "Hooliganz"'
        elif ID_Clan == 3:
            clan = 'Ты в клане "Lash and Fire"'
        elif ID_Clan == 4:
            clan = 'Ты в клане "Дикая жуть"'
        else:
            clan = ''
        info = MySQL.show("Subscription_Rock, Subscription_Energi, Time_KZ, Time_energi, Name0",message.from_user.id)

        subscription_Rock = info[0][0]          # считываем подписку на камни
        subscription_Energi = info[0][1]        # считываем подписку на энергию
        smena_KZ = str(int(info[0][2])+3)       # считываем смену кз
        sbor_energi = str(int(info[0][3])+3)    # считываем сбор энергии
        if subscription_Rock == 0:
            subscription_Rock_text = "Вы не подписаны на оповещение по камням."
        else:
            subscription_Rock_text = "Вы подписаны на оповещение по камням."
        if subscription_Energi == 0:
            subscription_Energi_text = "Вы не подписаны на оповещение по сбору энергии."
        else:
            subscription_Energi_text = "Вы подписаны на оповещение по сбору энергии."
        bot.send_message(message.from_user.id, "Твой ник в игре: " +info[0][4] + "\n" +subscription_Rock_text + "\n" +subscription_Energi_text + "\nВремя смены КЗ: "+smena_KZ + ":30 по мск \nВремя сбора первой энергии: " + sbor_energi + ":00 по мск\n"+clan)
    elif "Поменять время смены КЗ" == message.text:
        button.cancel_button(message,"Во сколько по москве смена КЗ? Вводи только час.\n Пример: \"18\"")
        bot.register_next_step_handler(message,MySQL.time_zone,2)
    elif "Поменять время первого сбора энергии" == message.text:
        button.cancel_button(message,"Во сколько по москве первый сбор энергии (синька и фиолетка)? Вводи только час.\n Пример: \"12\"")
        bot.register_next_step_handler(message,MySQL.time_zone,5)
    elif "Инструкция по применению" == message.text:
        with open('help/Instructions_for_use.txt','r') as file:
            text = file.read()
            file.close
        bot.send_message(message.from_user.id, text)
    elif "Инструкция для подключения меня к чату" == message.text:
        with open('help/Instructions_for_implementing_the_bot_in_the_chat.txt','r') as file:
            text = file.read()
            file.close
        bot.send_message(message.from_user.id, text)
    elif "Основные команды в чате" == message.text or ("люц" in message.text.lower() and ("команды" in message.text.lower() or (("что" in message.text.lower() or "че" in message.text.lower() or "чё" in message.text.lower() or "чо" in message.text.lower()) and "умеешь" in message.text.lower()))):
        with open('help/Basic_commands_in_the_chat.txt','r') as file:
            text = file.read()
            file.close
        bot.send_message(message.chat.id, text)
    elif "Инструкция по КВ" == message.text:
        manul_kv(message)
    elif "Расписание клановых заданий" == message.text:
        schedule_of_clan_tasks(message)
    elif "Полезные ссылки" == message.text:
        useful_links(message)
    elif "дата х2" == message.text.lower:
        date_x2(message)
    elif "Гайд по аптечкам в КВ" == message.text:
        manul_aptechkam_kv(message)
    elif "Необходимые герои для ивентов" == message.text:
        necessary_heroes_for_events(message)
    elif "Маницпуляции с героем" == message.text:
        button.setting_hiro_button(message, "Тут ты можешь добавить или удалить героя, ну и при необходимости переименовать его")
    elif "Подписки..." == message.text:
        button.Subscription_button(message, "Смотри...")
    elif "Поменять время..." == message.text:
        button.edit_time_button(message, "Меняй...")
    # elif "йцу" == message.text or "qwe" == message.text:
    #     bot.send_message( -1001378825774,"привет")#
    # elif message.chat.id ==  -1001378825774:
    #     bot.send_message(943180118, message)
    else:
        chatterbox.get_chat_text_messages(message)

@bot.message_handler(content_types=['sticker'])
def get_sticer_messages(message):
    if message.chat.type == "private":
        bot.send_message(message.from_user.id,"Прикольный стикер)")
#
#Эта команда дает знать проге, что она должна не прерывно слушать
#
Thread(target=time_loop, args=()).start()
bot.polling(none_stop=True, interval=0)

