from loader import bot
from database import db
import requests
from telebot import types

EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/"

class CurrencyBot:
    def __init__(self, bot_instance):
        self.bot = bot_instance

    def get_exchange_rate(self, base_currency, target_currency):
        """
        Получает курс валют с использованием внешнего API.
        """
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

    def send_welcome(self, message):
        """
        Приветственное сообщение при запуске команды /start.
        """
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        markup.add('EUR/USD', 'GBP/USD', 'AUD/USD', 'USD/RUB', 'История запросов')
        self.bot.reply_to(
            message,
            "Привет! Я бот для отслеживания курса валют.\nВыберите валютную пару или введите команду в формате:\n"
            "`/exchange USD RUB`",
            parse_mode='Markdown',
            reply_markup=markup
        )

    def exchange_rate(self, message):
        """
        Обрабатывает команду /exchange для получения курса по заданным валютам.
        """
        try:
            _, base_currency, target_currency = message.text.split()
            rate = self.get_exchange_rate(base_currency.upper(), target_currency.upper())
            if rate:
                response = f"Курс {base_currency.upper()} к {target_currency.upper()} = {rate}"
                self.bot.reply_to(message, response)
                
                # Сохраняем запрос в историю
                db.add_history(message.chat.id, f"{base_currency} -> {target_currency}", response)
            else:
                self.bot.reply_to(message, "Не удалось получить курс валют. Проверьте правильность ввода.")
        except ValueError:
            self.bot.reply_to(message, "Неверный формат команды. Введите в формате: /exchange USD RUB")
        except Exception as e:
            self.bot.reply_to(message, f"Произошла ошибка: {e}")

    def handle_currency_buttons(self, message):
        """
        Обрабатывает нажатия на кнопки с валютными парами и историей запросов.
        """
        currency_pairs = {
            'EUR/USD': ('EUR', 'USD'),
            'GBP/USD': ('GBP', 'USD'),
            'AUD/USD': ('AUD', 'USD'),
            'USD/RUB': ('USD', 'RUB')
        }
        
        if message.text in currency_pairs:
            base, target = currency_pairs[message.text]
            rate = self.get_exchange_rate(base, target)
            if rate:
                response = f"Курс {base} к {target} = {rate}"
                self.bot.send_message(message.chat.id, response)
                
                # Сохраняем запрос в историю
                db.add_history(message.chat.id, f"{base} -> {target}", response)
            else:
                self.bot.send_message(message.chat.id, "Не удалось получить курс для выбранной пары.")
        elif message.text == 'История запросов':
            self.show_history(message)

    def show_history(self, message):
        """
        Показывает последние 10 запросов пользователя.
        """
        history = db.get_last_history(message.chat.id)
        if history:
            history_text = "\n\n".join(
                [f"Запрос: {query}\nОтвет: {response}\nВремя: {timestamp}" for query, response, timestamp in history]
            )
        else:
            history_text = "История запросов пуста."

        self.bot.send_message(message.chat.id, history_text)

    def register_handlers(self):
        """
        Регистрируем обработчики команд и сообщений.
        """
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(commands=['exchange'])(self.exchange_rate)
        self.bot.message_handler(func=lambda message: True)(self.handle_currency_buttons)


currency_bot = CurrencyBot(bot)
currency_bot.register_handlers()