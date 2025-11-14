import os
import telebot
import requests

chat_id_save = []
HELPER = """
This is help menu:
/make_me_rich <p1p2...>	- Получить доступ к управлению кошельком
/check_api		- Проверка работоспособности впски
/reminder 		- Помогает вспомнить номер 7
/auth <password>	- Аутентификация
/help 			- Вызовет этот список
"""
FLAG = r'ZN2025{<flag>}'

def check_and_auth(chat_id, password):

    if chat_id not in chat_id_save:
        if password == 'LH179o2LQPH8':
            chat_id_save.append(chat_id)
        else:
            return False
    return True

def check_Oleg(chat_id, auth_text):
    try:
        password = auth_text.split(' ')[1]
    except:
        password = ''

    if not check_and_auth(chat_id, password):
        return "Ты не Олег! Олег бы знал пароль."
    else:
        return "Hello there!"

def perform_health_check():
    url = os.environ['URL'] + '/health'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.url + '\n' + response.text
        else:
            return response.url + '\n' + response.text
    except requests.exceptions.RequestException as e:
        return response


def check_seed_phrase(text):
    try:
        seedphrase = text.split(' ')[0]
    except:
        return False

    if seedphrase == os.environ['SEED']:
        return True
    return False

bot = telebot.TeleBot('tg_token')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! Я помогаю Олегу торговать криптой')

@bot.message_handler(commands=["help"])
def start(m, res=False):
    bot.send_message(m.chat.id, HELPER)

@bot.message_handler(commands=["auth"])
def start(m, res=False):
    bot.send_message(m.chat.id, check_Oleg(m.chat.id, m.text))

@bot.message_handler(commands=["reminder"])
def start(m, res=False):
    if check_and_auth(m.chat.id, m.text):
         bot.send_message(m.chat.id, f"Remember: {os.environ['REMINDER7']}")
    else:
         bot.send_message(m.chat.id, "Ты не Олег. Используй /help")

@bot.message_handler(commands=["make_me_rich"])
def start(m, res=False):
    if check_and_auth(m.chat.id, m.text):
        if (check_seed_phrase(m.text)):
            bot.send_message(m.chat.id, FLAG)
        else:
            bot.send_message(m.chat.id, "Неверная фраза. Надо писать подряд без пробелов.")
    else:
        bot.send_message(m.chat.id, "Ты не Олег. Используй /help")

@bot.message_handler(commands=["check_api"])
def start(m, res=False):
    if check_and_auth(m.chat.id, m.text):
        bot.send_message(m.chat.id, perform_health_check())
    else:
        bot.send_message(m.chat.id, "Ты не Олег. Используй /help")

@bot.message_handler(content_types=["text"])
def handle_text(m):
    if not check_and_auth(m.chat.id, m.text):
        bot.send_message(m.chat.id, "Олег, я тебя внимательно слушаю. Выбери команду из списка.")
    else:
        bot.send_message(m.chat.id, "Ты не Олег. Используй /help")

bot.polling(none_stop=True, interval=0)
