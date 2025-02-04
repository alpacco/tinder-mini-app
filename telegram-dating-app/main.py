from flask import Flask, request, jsonify, redirect, send_from_directory
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from telebot import TeleBot  # Для создания экземпляра бота
import telebot  # Для дополнительных классов и методов
from telebot.types import WebAppInfo
import logging
import json

# Загружаем переменные окружения
load_dotenv()

# Создаем экземпляр Flask
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# Получаем токен бота из .env
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = TeleBot(BOT_TOKEN)  # Создаем экземпляр бота

@app.route('/')
def index():
    return "Telegram Dating App is running!"

@app.route('/start')
def start():
    chat_id = request.args.get('chat_id')
    if chat_id:
        web_app_url = f"{request.url_root}mini-app/"
        web_app = WebAppInfo(url=web_app_url)
        try:
            bot.send_message(chat_id, "Привет! Нажми на кнопку ниже", reply_markup=web_app)
            app.logger.info(f"Sent message to chat ID: {chat_id}")
        except telebot.apihelper.ApiTelegramException as e:
            app.logger.error(f"Failed to send message to chat ID {chat_id}: {str(e)}")
    return redirect(f"https://t.me/{bot.user.username}?start=1")

@app.route('/mini-app/')
def mini_app():
    return send_from_directory('static', 'index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_string = request.get_data().decode('utf-8')
        app.logger.info(f"Raw update data: {json_string}")

        # Десериализуем данные
        update = telebot.types.Update.de_json(json_string)
        app.logger.info(f"Deserialized update: {update}")

        if update.message and update.message.text == '/start':
            app.logger.info("Received /start command")
            
            # Извлечение chat_id
            chat_id = update.message.chat.id
            app.logger.info(f"Extracted chat ID: {chat_id}")

            if not chat_id:
                app.logger.error("Chat ID is missing or invalid")
                return ''

            try:
                # Создание кнопки с Mini App
                web_app_url = f"{request.url_root}mini-app/"
                web_app = WebAppInfo(url=web_app_url)
                keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                keyboard.add(telebot.types.KeyboardButton(text="Открыть Mini App", web_app=web_app))

                # Отправка сообщения с кнопкой
                bot.send_message(chat_id, "Привет! Нажми на кнопку ниже", reply_markup=keyboard)
                app.logger.info("Message with WebApp button sent successfully")
            except Exception as e:
                app.logger.error(f"Failed to send message with WebApp button: {str(e)}")

        elif update.web_app_data:
            # Обработка данных из Mini App
            web_app_data = update.web_app_data.data
            app.logger.info(f"Received web app data: {web_app_data}")
            parsed_data = json.loads(web_app_data)

            if parsed_data.get('action') == 'save_profile':
                profile_data = parsed_data.get('data', {})
                app.logger.info(f"Saving profile data: {profile_data}")

                conn = get_db_connection()
                try:
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE users
                            SET data = %s
                            WHERE telegram_id = %s;
                        """, (json.dumps(profile_data), update.message.chat.id))
                        conn.commit()
                finally:
                    conn.close()

                bot.send_message(update.message.chat.id, "Профиль успешно сохранён!")

        bot.process_new_updates([update])
        return ''
    except Exception as e:
        app.logger.error(f"Error in webhook: {str(e)}")
        return 'Error', 500

def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        app.logger.info("Database connection successful")
        return conn
    except psycopg2.OperationalError as e:
        app.logger.error(f"Database connection failed: {str(e)}")
        raise
    except Exception as e:
        app.logger.error(f"Unexpected error during database connection: {str(e)}")
        raise

if __name__ == '__main__':
    app.run(debug=True)