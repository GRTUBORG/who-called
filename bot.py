import requests
import json
import telebot
import time

from telebot import types
from datetime import datetime, date, timedelta


token = os.environ.get('bot_token')
bot = telebot.TeleBot(str(token))
print('Бот работает!')

@bot.message_handler(commands = ['start'])
def start_command(message):
    str_countes = ''
    countes = [f'{message.from_user.id} — ID,\n',
               f'{message.from_user.first_name} — имя,\n',
               f'{message.from_user.last_name} — фамилия,\n',
               f'{message.from_user.username} — username.'
              ]
    for x in countes:
        str_countes += x
    bot.send_message(767815871, f'У тебя +1 новый пользователь! \n{str_countes}')
    bot.reply_to(message, "Рад тебя видеть! Просто скинь мне номер телефона (`через +`) и я дам тебе по нему информацию")
    
@bot.message_handler(content_types = ['text'])
def text(message):
    if len(message.text) == 12:
        phone = message.text
        getInfo = 'https://htmlweb.ru/geo/api.php?json&telcod={}'.format(phone)
        infoPhone = requests.get(getInfo)
    
        try:
            infoPhone = infoPhone.json()
            country = infoPhone["country"]["name"]
            region = infoPhone["region"]["name"]
            operator = infoPhone["0"]["oper"]
            oper_brand = infoPhone["0"]["oper_brand"]

            write = (f'*Результаты для номера телефона* `{phone}`\n\n'
                     f'• Страна: `{country}`,\n'
                     f'• Регион: `{region}`,\n'
                     f'• Оператор: {operator} ({oper_brand}).\n\n'
                     '[Поиск по объявлениям](https://big-bro.su/searh_by_phone.aspx)')
        except:
           write = 'Ошибка при распознавании номера телефона! \nПопробуйте ввести номер телефона через `+`, с другим кодом, или же проверьте код области!' 
        
        bot.send_message(message.chat.id, write, parse_mode = 'Markdown')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, *проверьте длину номера* телефона и попробуйте заново!', parse_mode = 'Markdown')
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop = True)
        except Exception as e:
            time.sleep(3)
            print(f'Возникла ошибка: {e}')
