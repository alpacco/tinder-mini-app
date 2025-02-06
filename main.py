import telebot
from telebot.types import WebAppInfo
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Замените YOUR_BOT_TOKEN на токен вашего бота
BOT_TOKEN = "7876864114:AAFVKi6_1oPLPzE6jRf_9O0IO7GzNjTjDzo"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        # Создаем кнопку для открытия Mini App
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        web_app_url = "https://tinder-mini-app-alpacco.amvera.io"  # Укажите URL вашего Mini App
        web_app_button = telebot.types.KeyboardButton(
            text="Open Seliger Tinder",
            web_app=WebAppInfo(url=web_app_url)
        )
        keyboard.add(web_app_button)

        # Отправляем сообщение с кнопкой
        bot.send_message(
            message.chat.id,
            "Добро пожаловать в Seliger Tinder! Нажмите кнопку ниже, чтобы начать.",
            reply_markup=keyboard
        )
        logger.info(f"Message sent to chat ID: {message.chat.id}")
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")

# Запуск бота
if __name__ == '__main__':
    bot.polling()