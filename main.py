import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Замените 'YOUR_BOT_TOKEN' на ваш токен
BOT_TOKEN = '7876864114:AAFVKi6_1oPLPzE6jRf_9O0IO7GzNjTjDzo'
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру с кнопкой для открытия Mini App
    keyboard = InlineKeyboardMarkup()
    web_app_url = "https://your-mini-app-url.amvera.app"  # Замените на URL вашего Mini App
    web_app_button = InlineKeyboardButton(
        text="Open Mini App",
        web_app=telebot.types.WebAppInfo(url=web_app_url)
    )
    keyboard.add(web_app_button)

    # Отправляем сообщение с кнопкой
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Нажмите кнопку ниже, чтобы открыть Mini App.",
        reply_markup=keyboard
    )

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)