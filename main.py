from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import sqlite3
import logging
from dotenv import load_dotenv
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),  # Логи будут записываться в файл bot.log
        logging.StreamHandler()          # Логи также будут выводиться в терминал
    ]
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('dating_app.db')
    cursor = conn.cursor()

    # Создаем таблицу пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            age INTEGER,
            interests TEXT,
            likes TEXT DEFAULT '',  -- Список ID пользователей, которым поставили лайк
            dislikes TEXT DEFAULT '',  -- Список ID пользователей, которым поставили дизлайк
            photos TEXT DEFAULT '',  -- Ссылки на фотографии профиля
            privacy TEXT DEFAULT 'public'  -- Настройка приватности (public/private)
        )
    ''')

    # Создаем таблицу для блокировок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            blocker_id INTEGER,
            blocked_id INTEGER,
            PRIMARY KEY (blocker_id, blocked_id)
        )
    ''')

    # Создаем таблицу для сообщений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Получение случайного пользователя для просмотра
def get_random_user(current_user_id):
    conn = sqlite3.connect('dating_app.db')
    cursor = conn.cursor()

    # Получаем случайного пользователя, исключая текущего
    cursor.execute('''
        SELECT user_id, name, age, interests, photos FROM users WHERE user_id != ?
        ORDER BY RANDOM() LIMIT 1
    ''', (current_user_id,))
    user = cursor.fetchone()
    conn.close()

    return user

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Это бот для знакомств. Используйте /register для регистрации.")

# Обработчик команды /register
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    conn = sqlite3.connect('dating_app.db')
    cursor = conn.cursor()

    # Проверяем, зарегистрирован ли пользователь
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if cursor.fetchone():
        await update.message.reply_text("Вы уже зарегистрированы!")
    else:
        # Регистрируем нового пользователя
        cursor.execute('''
            INSERT INTO users (user_id, name) VALUES (?, ?)
        ''', (user_id, user_name))
        conn.commit()
        await update.message.reply_text(
            f"Вы зарегистрированы, {user_name}! Теперь вы можете начать знакомиться с другими пользователями."
        )

    conn.close()

# Обработчик команды /profile
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    conn = sqlite3.connect('dating_app.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name, age, interests, photos FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        await update.message.reply_text("Вы не зарегистрированы. Используйте /register.")
        return

    name, age, interests, photos = user
    message = f"Имя: {name}\nВозраст: {age}\nИнтересы: {interests}"
    if photos:
        photo_url = photos.split(',')[0]
        await update.message.reply_photo(photo=photo_url, caption=message)
    else:
        await update.message.reply_text(message)

# Обработчик команды /edit_profile_web
async def edit_profile_web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Проверяем, зарегистрирован ли пользователь
    conn = sqlite3.connect('dating_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if not cursor.fetchone():
        await update.message.reply_text("Вы не зарегистрированы. Используйте /register.")
        conn.close()
        return

    # Создаем кнопку для открытия Web App
    keyboard = [
        [InlineKeyboardButton(
            "Редактировать профиль",
            web_app=WebAppInfo(url="http://alexeekt.beget.tech/myTelegramBot/webapp/index.html")
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Нажмите кнопку ниже, чтобы открыть веб-интерфейс для редактирования профиля:",
        reply_markup=reply_markup
    )
    conn.close()

# Обработчик команды /send_message
async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    args = context.args

    if len(args) < 2:
        await update.message.reply_text("Использование: /send_message <ID получателя> <текст>")
        return

    receiver_id = int(args[0])
    message_text = " ".join(args[1:])

    conn = sqlite3.connect('dating_app.db')
    cursor = conn.cursor()

    # Сохраняем сообщение в базу данных
    cursor.execute('''
        INSERT INTO messages (sender_id, receiver_id, message)
        VALUES (?, ?, ?)
    ''', (user_id, receiver_id, message_text))

    conn.commit()
    conn.close()

    await update.message.reply_text("Сообщение отправлено!")

# Обработчик команды /view_messages
async def view_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    conn = sqlite3.connect('dating_app.db')
    cursor = conn.cursor()

    # Получаем сообщения для пользователя
    cursor.execute('''
        SELECT sender_id, message, timestamp FROM messages
        WHERE receiver_id = ?
        ORDER BY timestamp DESC
    ''', (user_id,))
    messages = cursor.fetchall()
    conn.close()

    if not messages:
        await update.message.reply_text("У вас нет новых сообщений.")
        return

    for sender_id, message, timestamp in messages:
        await update.message.reply_text(f"От {sender_id} ({timestamp}):\n{message}")

# Обработчик команды /matches
async def matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    conn = sqlite3.connect('dating_app.db')
    cursor = conn.cursor()

    # Получаем список лайков пользователя
    cursor.execute('SELECT likes FROM users WHERE user_id = ?', (user_id,))
    likes = cursor.fetchone()[0] or ''
    likes = likes.split(',')

    # Находим взаимные лайки
    mutual_likes = []
    for liked_user_id in likes:
        if not liked_user_id.isdigit():
            continue
        cursor.execute('SELECT likes FROM users WHERE user_id = ?', (int(liked_user_id),))
        target_likes = cursor.fetchone()[0] or ''
        if str(user_id) in target_likes.split(','):
            mutual_likes.append(int(liked_user_id))

    conn.close()

    if not mutual_likes:
        await update.message.reply_text("У вас пока нет матчей.")
        return

    message = "Ваши матчи:\n"
    for match_id in mutual_likes:
        message += f"- ID: {match_id}\n"

    await update.message.reply_text(message)

# Обработчик команды /cleanup_messages
async def cleanup_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    conn = sqlite3.connect('dating_app.db')
    cursor = conn.cursor()

    # Удаляем сообщения старше 30 дней
    cursor.execute('''
        DELETE FROM messages
        WHERE timestamp < datetime('now', '-30 days')
    ''')

    conn.commit()
    conn.close()

    await update.message.reply_text("Старые сообщения успешно удалены.")

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Доступные команды:\n"
        "/start - Начало работы\n"
        "/register - Регистрация\n"
        "/profile - Просмотреть профиль\n"
        "/edit_profile_web - Редактировать профиль через Web App\n"
        "/matches - Просмотреть матчи\n"
        "/send_message <ID> <текст> - Отправить сообщение\n"
        "/view_messages - Просмотреть сообщения\n"
        "/cleanup_messages - Очистить старые сообщения\n"
        "/help - Список команд"
    )
    await update.message.reply_text(help_text)

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Основная функция
def main():
    init_db()

    application = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("edit_profile_web", edit_profile_web))
    application.add_handler(CommandHandler("send_message", send_message))
    application.add_handler(CommandHandler("view_messages", view_messages))
    application.add_handler(CommandHandler("matches", matches))
    application.add_handler(CommandHandler("cleanup_messages", cleanup_messages))
    application.add_handler(CommandHandler("help", help_command))

    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == '__main__':
    main()