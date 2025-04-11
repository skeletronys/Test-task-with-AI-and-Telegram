import telebot
import os
from dotenv import load_dotenv
from agent.langchain_agent import create_agent
from agent.search_tool import search_google

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# create agent
agent = create_agent()

# save session
user_sessions = {}


@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, "Привіт! Я AI-консультант автосалону AutoDream. Питайте що вас цікавить")


@bot.message_handler(commands=["search"])
def search_handler(message):
    user_id = message.chat.id
    query = message.text.replace("/search", "").strip()

    if not query:
        bot.send_message(user_id, "Введи пошуковий запит, наприклад:\n/search Tesla Model 3 в Україні")
        return

    bot.send_message(user_id, f"Шукаю в Google: *{query}*", parse_mode="Markdown")
    try:
        result = search_google(query)
        bot.send_message(user_id, result, disable_web_page_preview=True)
    except Exception as e:
        print(f"[SEARCH ERROR] {e}")
        bot.send_message(user_id, "Сталася помилка під час пошуку")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_input = message.text

    try:
        # answer
        response = agent.run(user_input)
        bot.send_message(user_id, response)

    except Exception as e:
        print(f"[ERROR] {e}")
        bot.send_message(user_id, "Вибачте, щось пішло не так. Спробуйте ще раз.")

if __name__ == "__main__":
    print("Бот запущено та готовий до відповідей")
    bot.polling()
