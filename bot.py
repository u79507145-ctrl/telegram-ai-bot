import os
import telebot
from openai import OpenAI

# Токены берём из переменных окружения (НЕ пишем их в код!)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Нет TELEGRAM_TOKEN или OPENAI_API_KEY. Задай их в настройках хостинга.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def start_cmd(msg):
    bot.reply_to(msg, "Привет! Я ИИ-бот. Спроси меня что угодно ✨")

@bot.message_handler(func=lambda m: True)
def handle(msg):
    try:
        # Запрашиваем ответ у OpenAI
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg.text}],
        )
        text = resp.choices[0].message.content or "Пустой ответ 🤔"

        # Телеграм ограничивает ~4096 символов — режем длинные
        for i in range(0, len(text), 4000):
            bot.reply_to(msg, text[i:i+4000])

    except Exception as e:
        bot.reply_to(msg, f"Ошибка: {e}")

print("🤖 Бот запущен (polling)…")
bot.infinity_polling(skip_pending=True)
