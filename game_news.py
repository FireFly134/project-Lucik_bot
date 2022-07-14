import json

import requests
from bs4 import BeautifulSoup

import telegram

with open('token.txt', 'r') as file:
    token = file.read()
bot = telegram.Bot(token)

def post():
    link = "https://vk.com/ageofmagicgame"

    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }

    sait = requests.get(link, headers=header).text

    soup = BeautifulSoup(sait, "lxml")
    post_link = soup.find("a", class_="post_link").get('href')
    try:
        with open('data.json') as json_file:
            post_link_old = json.load(json_file)
    except Exception:
        post_link_old = "none link"

    if post_link_old != post_link:
        with open('data.json', 'w') as outfile:
            json.dump(post_link, outfile)  # _save

        text_post = soup.find("div", class_="wall_text")

        sms = str(sms_post(text_post))
        link_img_post = text_post.find_all("a")
        i = len(link_img_post) - 1
        N = len(link_img_post[i].get('style')) - 2
        link_img = link_img_post[i].get('style')[50:N]
        img = requests.get(link_img, verify=False).content
        with open("img.jpg", "wb") as image:
            image.write(img)
        try:
            photo = open('img.jpg', 'rb')
            bot.send_photo('-1001317835865', photo, sms + "\n" + "https://vk.com" + post_link)
            print(sms + "\n" + "https://vk.com" + post_link)
        except:
            try:
                bot.send_message('-1001317835865', sms)
                print(sms)
                photo = open('img.jpg', 'rb')
                bot.send_photo('-1001317835865', photo, "https://vk.com" + post_link)
                print("https://vk.com" + post_link)
            except:
                pass
                # bot.send_message(admins[0][0],
                #                  "ERROR: Пост новостей для чата с ID = " + str(Chat[i]) + " не пришел!")
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

if __name__ == "__main__":
    post()