import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, ConvertioException

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'чтобы перевести валюту, введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевест> \
<количество переводимой валюты>\n<посмотреть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertioException('Не верное количество параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertioException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()

# response = requests.get(
#     "https://v6.exchangerate-api.com/v6/76253a19656d5894b69c8e6f/pair/EUR/USD/1"
# )
# print(response.status_code)
# print(response.json())


# @bot.message_handler()
# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'helo')
#
# bot.polling()





