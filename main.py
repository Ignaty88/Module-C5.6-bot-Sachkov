
import telebot
from conf import keys, TOKEN
from extensions import CriptoConvertor, ConvertionExeption

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username} чтобы начать работу, \n "
                                      f"введите боту команду в одно сообщение в следующем формате: \n "
                                      f"  'имя валюты' 'валюта в которую переводим' 'количество'\n "
                                      f"--------------------------------------------------\n"
                                      f"Чтобы увидеть список всех валют введите: /values ")


@bot.message_handler(commands=['values'])
def val(message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n" .join((text, key))
    bot.reply_to(message, text)


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
