import config
import logging
from random import randint
import aiogram.utils.markdown as fmt
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# log
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
button_hi = KeyboardButton('Привет! 👋')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)
# prices
PRICE = types.LabeledPrice(label="Курс Яндекс лицей Unity", amount=500 * 100)  # в копейках (руб)

'''
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=kb.greet_kb)'''


@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)


@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Купить курсы", "Заметки", "GPT", "Новости"]
    keyboard.add(*buttons)
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "GPT")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")
    '''
    await bot.send_invoice(message.chat.id,
                           title="Продажа IT курсов по приятным ценам",
                           description=f"Каталог \n Курс Яндекс лицей Unity: /UnityBuy \n"
                                       f"Курс питон: /PythonBuy \n Rest api курс: /RestBuy \n"
                                       f"Курс After Effects: /AfterBuy",
                           photo_url="https://obshestvo.org/wp-content/uploads/2020/08/yl.jpg",
                           photo_width=600,
                           photo_height=450,
                           photo_size=600,
                           is_flexible=False)
    await bot.send_message(message.chat.id, f"Каталог \n Курс Яндекс лицей Unity: /buy")
    '''
    '''
    @bot.message_handler(commands=['start'])
    def start(msg):
        mess = f'Привет, {msg.from_user.first_name}!'
        bot.send_message(msg.chat.id, mess, parse_mode='html')
        bot.send_message(msg.chat.id, f'Читать свежие новости /NewsStart', parse_mode='html')
        bot.send_message(msg.chat.id, f'Ваши заметки /YourNotes', parse_mode='html')
        bot.send_message(msg.chat.id, f'Советы для программиста /Tips', parse_mode='html')'''


@dp.message_handler(commands=['UnityBuy'])
async def UnityBuy(message: types.Message):
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

    # run long-polling


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
