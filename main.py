import requests
import telebot
from telebot import types
from bs4 import BeautifulSoup as b

TLG_key = '5701152954:AAFlBLwPa0BYw5m9zHwEQetmmZAoCyvd8B0'
URL = 'https://www.ixbt.com/news/'


def parser(url):
    r = requests.get(URL)
    soup = b(r.text, 'html.parser')
    news = soup.find_all('strong', class_='')
    return [c.text for c in news]


def parser2(url):
    r = requests.get(URL)
    soup = b(r.text, 'html.parser')
    dskrnews = soup.find_all('div', class_='item__text__top')
    return [c.text for c in dskrnews]


def parser3(url):
    r = requests.get(URL)
    soup = b(r.text, 'html.parser')
    time = soup.find_all('span', class_='time_iteration_icon_light')
    return [c.text for c in time]


News = parser(URL)
NewsM = News[:3]
NewsD = News[3:]
Dskr = parser2(URL)
Time = parser3(URL)
TimeD = Time[3:]
TimeM = Time[:3]
bot = telebot.TeleBot(TLG_key)


@bot.message_handler(commands=['start'])


def start(msg):
    mess = f'Привет, {msg.from_user.first_name}!'
    bot.send_message(msg.chat.id, mess, parse_mode='html')
    bot.send_message(msg.chat.id, f'Читать свежие новости /NewsStart', parse_mode='html')
    bot.send_message(msg.chat.id, f'Ваши заметки /YourNotes', parse_mode='html')
    bot.send_message(msg.chat.id, f'Советы для программиста /Tips', parse_mode='html')


@bot.message_handler(commands=['YourNotes'])


def YourNotes(msg):
    bot.send_message(msg.chat.id, 'В разработке', parse_mode='html')
    bot.send_message(msg.chat.id, 'Вернуться в главное меню /start', parse_mode='html')


@bot.message_handler(commands=['Tips'])


def Tips(msg):
    bot.send_message(msg.chat.id, 'В разработке', parse_mode='html')
    bot.send_message(msg.chat.id, 'Вернуться в главное меню /start', parse_mode='html')


@bot.message_handler(commands=['NewsStart'])


def newsStart(msg):
    global NewsM
    global NewsD
    global TimeM
    global TimeD
    global Dskr
    mess = f'Новости'
    bot.send_message(msg.chat.id, mess, parse_mode='html')
    NewsM = News[:3]
    TimeM = Time[:3]
    NewsD = News[3:]
    TimeD = Time[3:]
    Dskr = parser2(URL)
    bot.send_message(msg.chat.id, 'Читать главные новости: /newsMain', parse_mode='html')
    bot.send_message(msg.chat.id, 'Читать другие новости: /news', parse_mode='html')


@bot.message_handler(commands=['newsMain'])


def newsMain(message):
    if len(NewsM) == 0:
        bot.send_message(message.chat.id, 'Главных новостей больше нет.')
        bot.send_message(message.chat.id, 'Читать другие новости: /news')
        bot.send_message(message.chat.id, 'Обновление бота: /start')
    else:
        bot.send_message(message.chat.id, TimeM[0])
        del TimeM[0]
        bot.send_message(message.chat.id, NewsM[0])
        del NewsM[0]
        bot.send_message(message.chat.id, Dskr[0])
        del Dskr[0]
        bot.send_message(message.chat.id, 'Читать главные новости: /newsMain')
        bot.send_message(message.chat.id, 'Читать другие новости: /news')
        bot.send_message(message.chat.id, 'Читать статью полностью: /website')


@bot.message_handler(commands=['news'])


def news(message):
    if len(NewsD) == 0:
        bot.send_message(message.chat.id, 'новостей больше нет.')
        bot.send_message(message.chat.id, 'Обновление бота: /start')
    elif len(NewsM) == 0:
        bot.send_message(message.chat.id, TimeD[0])
        del TimeD[0]
        bot.send_message(message.chat.id, NewsD[0])
        del NewsD[0]
        bot.send_message(message.chat.id, 'Читать дальше: /news')
        bot.send_message(message.chat.id, 'Читать статью полностью: /website')
    else:
        bot.send_message(message.chat.id, TimeD[0])
        del TimeD[0]
        bot.send_message(message.chat.id, NewsD[0])
        del NewsD[0]
        bot.send_message(message.chat.id, 'Читать главные новости: /newsMain')
        bot.send_message(message.chat.id, 'Читать дальше: /news')
        bot.send_message(message.chat.id, 'Читать статью полностью: /website')


@bot.message_handler(commands=['website'])
def website(msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить веб сайт ixbt:", url="https://www.ixbt.com/news/"))
    bot.send_message(msg.chat.id, 'ixbt.com', reply_markup=markup)
    bot.send_message(msg.chat.id, 'Читать главные новости: /newsMain')
    bot.send_message(msg.chat.id, 'Чтобы продолжить читать новости нажмите сюда: /news')


bot.polling(none_stop=True)
