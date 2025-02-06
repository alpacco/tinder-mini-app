import telebot

# Замените YOUR_BOT_TOKEN на токен вашего бота
bot = telebot.TeleBot("876864114:AAFVKi6_1oPLPzE6jRf_9O0IO7GzNjTjDzoEN")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем кнопку для открытия Mini App
    keyboard = telebot.types.InlineKeyboardMarkup()
    open_app_button = telebot.types.InlineKeyboardButton(
        text="Open Seliger Tinder",
        web_app=telebot.types.WebAppInfo(url="https://tinder-mini-app-alpacco.amvera.io")
    )
    keyboard.add(open_app_button)

    # Отправляем приветственное сообщение с кнопкой
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в Seliger Tinder! Нажмите кнопку ниже, чтобы начать.",
        reply_markup=keyboard
    )

# Запуск бота
bot.polling()