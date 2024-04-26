import requests
import config
from asyncio import Lock
from random import randint
from telebot import types
from aiogram.dispatcher.storage import FSMContext
from yandexgptlite import YandexGPTLite
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup as b
from aiogram.types.message import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiogram.utils.markdown as fmt
import aiogram
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

URL = 'https://www.ixbt.com/news/'
bot = Bot(token="5701152954:AAFlBLwPa0BYw5m9zHwEQetmmZAoCyvd8B0", parse_mode='HTML')
account = YandexGPTLite('b1g7anst1rljuuojh34n', 'y0_AgAAAAAw_WLIAATuwQAAAAEDFR4xAABlYsGIquVPL4rSURTDk7KbdKFFQw')
dp = Dispatcher(bot, storage=MemoryStorage())
lock = Lock()


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
    data = soup.find_all('a', class_='comments_link')
    data = str(data).split('href="')
    for i in range(len(data)):
        prepare.append(data[i])
    for i in range(1, len(prepare)):
        ready = prepare[i].split('#')
        print(ready)
        readytosend.append(str(ready[0]))
    return [c for c in readytosend]


News = parser(URL)
NewsM = News[:3]
NewsD = News[3:]
Dskr = parser2(URL)
Time = parser3(URL)
Source = parser4(URL)
print(Source[0])
TimeD = Time[3:]
TimeM = Time[:3]


class RegisterMessages(StatesGroup):
    step1 = State()
    step2 = State()
    name = State()
    desc = State()
    dates = State()
    priority = State()


class DB:
    answer_data = {}
    all_notes = []
    name = ''
    descript = ''
    dates = ''
    priority = ''


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
    animation = types.InputFile('grandma.gif')
    await bot.send_animation(message.chat.id, animation=animation,
                             caption=f'Представьте Telegram-бота, который понимает вас с полуслова, ведет увлекательные'
                                     f' беседы и выполняет любые задачи. С GPT это реальность! \nGPT-боты общаются на естественном языке,'
                                     f' создают уникальный контент, переводят тексты, анализируют информацию и многое другое.'
                                     f' \nПовысьте эффективность бизнеса и удивите клиентов умным ботом с искусственным интеллектом GPT.')
    await RegisterMessages.step1.set()
    await bot.send_message(message.from_user.id, text='Введите запрос для GPT')


@dp.message_handler(content_types='text', state=RegisterMessages.step1)
async def reg_step1(message: types.Message, state: FSMContext):
    async with lock:
        DB.answer_data['name'] = message.text
    text = account.create_completion(DB.answer_data["name"], '0.6',
                                     system_prompt='Отвечай на русском')
    await bot.send_message(message.from_user.id, text=f'{text}\n\nЧтобы сделать еще один запрос нажмите на кнопку GPT')
    await state.finish()


@dp.message_handler(lambda message: message.text == "Заметки")
async def without_puree(message: types.Message):
    print(message)
    await message.reply("В разработке!")


@dp.message_handler(lambda message: message.text == "Новая заметка")
async def new_note(message: types.Message):
    print(DB.all_notes)
    sp = DB.all_notes

    await RegisterMessages.name.set()
    name = DB.name

    await RegisterMessages.desc.set()
    descr = DB.descript

    await RegisterMessages.dates.set()
    dates = DB.dates

    await RegisterMessages.priority.set()
    priority = DB.priority

    names = []
    if sp:
        ...
    else:
        for i in sp:
            names.append(i['names'])
    while name in names:
        await bot.send_message(message.from_user.id, text='такое название уже существует')
        await RegisterMessages.name.set()
        name = DB.name

    D = {'name': name,
         'description': descr,
         'priority': priority,
         'dates': dates}

    sp.append(D)
    DB.all_notes = sp
    DB.name = ''
    DB.dates = ''
    DB.priority = ''
    DB.descript = ''


@dp.message_handler(content_types='text', state=RegisterMessages.name)
async def get_name(message: types.Message, state: FSMContext):
    async with lock:
        DB.name = message.text
        await bot.send_message(message.from_user.id, text='Введите название')
        await state.finish()


@dp.message_handler(content_types='text', state=RegisterMessages.desc)
async def get_desc(message: types.Message, state: FSMContext):
    async with lock:
        DB.descript = message.text
        await bot.send_message(message.from_user.id, text='Введите описание')
        await state.finish()


@dp.message_handler(content_types='text', state=RegisterMessages.dates)
async def get_date(message: types.Message, state: FSMContext):
    async with lock:
        DB.dates = message.text
        await bot.send_message(message.from_user.id, text='Введите дедлайн')
        await state.finish()


@dp.message_handler(content_types='text', state=RegisterMessages.priority)
async def get_priority(message: types.Message, state: FSMContext):
    async with lock:
        DB.priority = message.text
        await bot.send_message(message.from_user.id, text='Введите приоритет')
        await state.finish()


@dp.message_handler(lambda message: message.text == "Купить курсы")
async def without_puree(message: types.Message):
    animation = types.InputFile('learn.gif')
    await bot.send_animation(message.chat.id, animation=animation,
                             caption=f'Хотите погрузиться в увлекательный мир информационных технологий и стать настоящим профессионалом в IT-сфере? '
                                     f'Мы поможем!\n\nПредлагаем вам учебные материалы от лучших специалистов, интерактивные задания,'
                                     f' практические проекты и поддержку на каждом этапе обучения.\n\nНаши программы помогут '
                                     f'вам не только освоить новые знания, но и применить их на практике, чтобы стать экспертом в своей области.')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Курс Яндекс лицей Unity", callback_data='unity'))
    keyboard.add(types.InlineKeyboardButton(text="Курс REST-api", callback_data='restapi'))
    keyboard.add(types.InlineKeyboardButton(text="Курс Python", callback_data='python'))
    await message.answer("Каталог курсов:", reply_markup=keyboard)


@dp.callback_query_handler(text="unity")
async def send_random_value(call: types.CallbackQuery):
    await call.answer(text="Ой-ой! Кажется тут нарушаются авторские права, сделайте вид как будто вы этого не знаете.",
                      show_alert=True)
    await call.message.answer("Я понимаю, что пиратсво это плохо\nПерейти к курсу /UnityBuy")


@dp.callback_query_handler(text="restapi")
async def send_random_value(call: types.CallbackQuery):
    await call.answer(text="Ой-ой! Кажется тут нарушаются авторские права, сделайте вид как будто вы этого не знаете.",
                      show_alert=True)
    await call.message.answer("Я понимаю, что пиратсво это плохо\nПерейти к курсу /RestBuy")


@dp.callback_query_handler(text="python")
async def send_random_value(call: types.CallbackQuery):
    await call.answer(text="Ой-ой! Кажется тут нарушаются авторские права, сделайте вид как будто вы этого не знаете.",
                      show_alert=True)
    await call.message.answer("Я понимаю, что пиратсво это плохо\nПерейти к курсу /PythonBuy")


@dp.message_handler(commands=['UnityBuy'])
async def UnityBuy(message: types.Message):
    PRICE = types.LabeledPrice(label="Курс Яндекс лицей Unity", amount=1000 * 100)  # в копейках (руб)
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


@dp.message_handler(commands=['RestBuy'])
async def UnityBuy(message: types.Message):
    PRICE = types.LabeledPrice(label="Курс Resp Api", amount=600 * 100)  # в копейках (руб)
    if config.PAYTOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Курс Resp Api")
    await bot.send_invoice(message.chat.id,
                           title="Курс Resp Api",
                           description="Ссылки на материал + видео-учебник",
                           provider_token=config.PAYTOKEN,
                           currency="rub",
                           photo_url="https://www.astera.com/wp-content/uploads/2020/01/rest.png",
                           photo_width=936,
                           photo_height=708,
                           photo_size=936,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="RestApiStep",
                           payload="RestApiStepBuy")


@dp.message_handler(commands=['PythonBuy'])
async def UnityBuy(message: types.Message):
    PRICE = types.LabeledPrice(label="Курс Python основы", amount=400 * 100)  # в копейках (руб)
    if config.PAYTOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Курс Python основы")
    await bot.send_invoice(message.chat.id,
                           title="Курс Python основы",
                           description="Ссылки на материал + видео-учебник",
                           provider_token=config.PAYTOKEN,
                           currency="rub",
                           photo_url="https://www.hse.ru/data/2019/09/12/1537849837/3%D0%BF%D0%B8%D1%82%D0%BE%D0%BD%20%D0%BB%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF.png",
                           photo_width=1083,
                           photo_height=722,
                           photo_size=1083,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="pythonbuy",
                           payload="PythonStepBuy")


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
    if message.successful_payment.total_amount // 100 == 1000:
        await bot.send_message(message.chat.id,
                               f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно! "
                               f"Ссылка: https://disk.yandex.ru/d/g721TvTNaXivig \n Не забудьте сохранить ссылку!")
    elif message.successful_payment.total_amount // 100 == 600:
        await bot.send_message(message.chat.id,
                               f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно! "
                               f"Ссылка: https://disk.yandex.ru/d/0KgkiFJVHW0Lrw\n\nНе забудьте сохранить ссылку!")
    elif message.successful_payment.total_amount // 100 == 400:
        await bot.send_message(message.chat.id,
                               f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно! "
                               f"Ссылка: https://disk.yandex.ru/d/7DjT3k8aI6H7Mg\n\nНе забудьте сохранить ссылку!")


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
