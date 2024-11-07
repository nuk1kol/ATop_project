# 7701242307:AAGCBbbKdUthratz6K8chD1rc_gMsY9C5kw
import telebot
import requests

# Вставьте сюда токен вашего бота
API_TOKEN = '7701242307:AAGCBbbKdUthratz6K8chD1rc_gMsY9C5kw'

# Создаем объект бота
bot = telebot.TeleBot(API_TOKEN)

# API для получения курса валют
EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/"

# Функция для получения курса валют
def get_exchange_rate(base_currency, target_currency):
    try:
        response = requests.get(f"{EXCHANGE_RATE_API_URL}{base_currency}")
        data = response.json()
        if 'rates' in data and target_currency in data['rates']:
            return data['rates'][target_currency]
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении курса валют: {e}")
        return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для отслеживания курса валют.\n"
                          "Введите команду в формате:\n"
                          "`/exchange USD RUB` - для получения курса USD к RUB.",
                 parse_mode='Markdown')

# Обработчик команды /exchange
@bot.message_handler(commands=['exchange'])
def exchange_rate(message):
    try:
        # Получаем текст команды и делим его на части
        _, base_currency, target_currency = message.text.split()
        
        # Получаем курс валют
        rate = get_exchange_rate(base_currency.upper(), target_currency.upper())
        
        # Проверяем, удалось ли получить курс
        if rate:
            bot.reply_to(message, f"Курс {base_currency.upper()} к {target_currency.upper()} = {rate}")
        else:
            bot.reply_to(message, "Не удалось получить курс валют. Проверьте правильность ввода.")
    except ValueError:
        bot.reply_to(message, "Неверный формат команды. Введите в формате: /exchange USD RUB")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Запускаем бота
bot.polling()