
import telebot
from conf import keys, TOKEN
from extensions import CriptoConvertor, ConvertionExeption
from telebot import types

conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
for val in keys.keys():
    buttons.append(types.KeyboardButton(val.lower()))

conv_markup.add(*buttons)


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username} чтобы начать работу, \n "
                                      f"введите боту команду в одно сообщение в следующем формате: \n "
                                      f"  'имя валюты' 'валюта в которую переводим' 'количество'\n "
                                      f"Или нажми /convert \n"
                                      f"--------------------------------------------------\n"
                                      f"Чтобы увидеть список всех валют введите: /values ")


@bot.message_handler(commands=['values'])
def val(message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n" .join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = "Выберите валюту из которой конвертировать"
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_step_handler(message, quote_handler,)

def quote_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = "Выберите валюту в которую конвертировать"
    bot.send_message(message.chat.id, text, reply_markup = conv_markup)
    bot.register_next_step_handler(message, base_handler,base)

def base_handler(message: telebot.types.Message,base):
    quote = message.text.strip()
    text = "Введите количество конвертируемой валюты"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        new_price = CriptoConvertor.get_price(base, quote, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка: \n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {new_price}'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def convert(massege: telebot.types.Message):
    values = massege.text.lower()

    try:
        values = values.split()

        if len(values) != 3:
            raise ConvertionExeption("Много параметров")

        quote, base, amount = values
        new_price = CriptoConvertor.get_price(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(massege, f'Ошибка: \n{e}')
    except Exception as e:
        bot.reply_to(massege, f'Не удалось обработать команду {e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {new_price}'
        bot.send_message(massege.chat.id, text)



bot.polling(none_stop=True)
