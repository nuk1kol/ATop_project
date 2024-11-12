from loader import bot
import user_handler

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)