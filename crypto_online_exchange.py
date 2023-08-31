import telebot
import requests
import json
from config import Keys, TOKEN
from utils import *

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.username}!\nЧтобы начать работу, "
                                      f"введите команду боту в следующем формате:\n"
                                      f"<Имя валюты> <В какую валюту хотите перевести> <Количество переводимой валюты>\n"
                                      f"Например: Bitcoin Dolar 10\n"
                                      f"Увидеть список доступных валют: /values")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in Keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        args = message.text.split()
        if len(args) != 3:
            raise FormatError()

        quote, base, amount = args
        if quote == base:
            raise SameCurrencyError()
        if quote not in Keys or base not in Keys:
            raise InvalidCurrencyError()
        if not amount.isdigit():
            raise InvalidAmountError()

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={Keys[quote]}&tsyms={Keys[base]}')
        data = json.loads(r.content)
        if Keys[base] in data:
            rate = data[Keys[base]]
            result = float(amount) * rate
            text = f'Цена {amount} {quote} в {base} - {result:.6f} {Keys[base]}'
            bot.send_message(message.chat.id, text)
        else:
            raise ConversionError("Не удалось получить курс")
    except ConversionError as e:
        bot.send_message(message.chat.id, str(e))
    except requests.exceptions.RequestException:
        bot.send_message(message.chat.id, "Произошла ошибка при запросе к серверу")


bot.polling(none_stop=True)
