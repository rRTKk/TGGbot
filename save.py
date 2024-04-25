'''
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
    global Source
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
'''