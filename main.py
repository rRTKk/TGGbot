import requests
import config
from random import randint
from telebot import types
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup as b
from aiogram.types.message import ContentType
import aiogram.utils.markdown as fmt
import aiogram
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

URL = 'https://www.ixbt.com/news/'
bot = Bot(token="5701152954:AAFlBLwPa0BYw5m9zHwEQetmmZAoCyvd8B0")
dp = Dispatcher(bot)


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


def parser4(url):
    prepare = []
    readytosend = []
    r = requests.get(URL)
    soup = b(r.text, 'html.parser')
    print(soup)
    data = soup.find_all('a', class_='comments_link')

    data = str(data).split('href="')
    for i in range(len(data)):
        if i % 2 == 1:
            prepare.append(data[i])
    for i in range(len(prepare)):
        ready = prepare[i].split('#')
        readytosend.append(str(ready[0]))
    return [c for c in readytosend]


def parser5(url):
    prepare = []
    readytosend = []
    r = requests.get(URL)
    soup = b(r.text, 'html.parser')
    data = soup.find_all('a', class_='time_iteration_icon_light')
    data = str(data).split('href="')
    for i in range(len(data)):
        if i % 2 == 1:
            prepare.append(data[i])
    for i in range(len(prepare)):
        ready = prepare[i].split('#')
        readytosend.append(str(ready[0]))
    return [c for c in readytosend]


News = parser(URL)
NewsM = News[:3]
NewsD = News[3:]
Dskr = parser2(URL)
Time = parser3(URL)
Source = parser4(URL)
SourceMain = parser5(URL)
print(SourceMain)
print(Source[0])
TimeD = Time[3:]
TimeM = Time[:3]


@dp.message_handler(commands="start")
async def start(message: types.Message):
    animation = types.InputFile('startvis.gif')
    await bot.send_animation(message.chat.id, animation=animation,
                             caption=f'Добро пожаловать, {message.from_user.first_name}! \n\nЭто бот для IT-энтузиастов!\n'
                                     f'Здесь ты сможешь быть в курсе последних новостей из мира информационных технологий,'
                                     f' приобрести доступ к качественным IT курсам, вести личный дневник и создавать напоминания.\n'
                                     f'Но это еще не все! Бот также оснащен нейросетью GPT, которая поможет ответить на любые вопросы и провести увлекательные беседы на тему IT. '
                                     f'\nПогружайся в мир технологий с нашим ботом и становись лучше каждый день!')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Купить курсы", "Заметки", "GPT", "Новости"]
    keyboard.add(*buttons)
    await message.answer("Чем могу быть полезен?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "GPT")
async def without_puree(message: types.Message):
    await message.reply("В разработке!")


@dp.message_handler(lambda message: message.text == "Заметки")
async def without_puree(message: types.Message):
    await message.reply("В разработке!")


@dp.message_handler(lambda message: message.text == "Купить курсы")
async def without_puree(message: types.Message):
    animation = types.InputFile('learn.gif')
    await bot.send_animation(message.chat.id, animation=animation,
                             caption=f'Хотите погрузиться в увлекательный мир информационных технологий и стать настоящим профессионалом в IT-сфере? '
                                     f'Мы поможем!\n\nПредлагаем вам учебные материалы от лучших специалистов, интерактивные задания,'
                                     f' практические проекты и поддержку на каждом этапе обучения.\n\nНаши программы помогут '
                                     f'вам не только освоить новые знания, но и применить их на практике, чтобы стать экспертом в своей области.')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Курс Яндекс лицей Unity", callback_data="random_value"))
    await message.answer("Каталог курсов", reply_markup=keyboard)

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.answer(text="Ой-ой! Кажется тут нарушаются авторские права, сделайте вид как будто вы этого не знаете.", show_alert=True)

@dp.message_handler(commands=['UnityBuy'])
async def UnityBuy(message: types.Message):
    PRICE = types.LabeledPrice(label="Курс Яндекс лицей Unity", amount=500 * 100)
    if config.PAYTOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Курс Яндекс лицей Unity")
    await bot.send_invoice(message.chat.id,
                           title="Курс Яндекс лицей Unity",
                           description="Ссылки на материал + видео-учебник",
                           provider_token=config.PAYTOKEN,
                           currency="rub",
                           photo_url="https://obshestvo.org/wp-content/uploads/2020/08/yl.jpg",
                           photo_width=600,
                           photo_height=450,
                           photo_size=600,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="Yandex_Unity",
                           payload="Yandex_Unity")


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

    # successful payment


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно! "
                           f"Ссылка: https://disk.yandex.ru/d/g721TvTNaXivig \n Не забудьте сохранить ссылку! \n"
                           f"Вернуться на главный экран \start")


@dp.message_handler(lambda message: message.text == "Новости")
async def news(message: types.Message):
    if len(NewsD) == 0:
        bot.send_message(message.chat.id, 'новостей больше нет.')
        bot.send_message(message.chat.id, 'Обновление бота: /start')
    elif len(NewsM) == 0:
        await message.answer(
            f"{fmt.hide_link(f'https://www.ixbt.com/{Source[0]}')}{TimeD[0]}: {NewsD[0]} \n\n"
            f'Чтобы прочитать следующую новость жми "Новости"\nЧтобы обновить новости жми "Перезагрузка"',
            parse_mode=types.ParseMode.HTML)

        del TimeD[0]
        del NewsD[0]
        del Source[0]
    else:
        await message.answer(
            f"{fmt.hide_link(f'https://www.ixbt.com/{Source[0]}')}{TimeD[0]}: {NewsD[0]} \n\n"
            f'Чтобы прочитать следующую новость жми "Новости"\nЧтобы обновить новости жми "Перезагрузка"',
            parse_mode=types.ParseMode.HTML)

        del TimeD[0]
        del NewsD[0]
        del Source[0]


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
