import telebot
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_input = message.text
    response = "Привіт! Я консультант автосалону. Як можу допомогти?"
    bot.send_message(user_id, response)


if __name__ == "__main__":
    print("Бот запущено")
    bot.polling()
