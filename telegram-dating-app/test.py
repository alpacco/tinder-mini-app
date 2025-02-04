import os
import psycopg2

# Получаем строку подключения из .env
DATABASE_URL = os.getenv('DATABASE_URL')

try:
    # Пытаемся подключиться к базе данных
    conn = psycopg2.connect(DATABASE_URL)
    print("Подключение успешно!")
    conn.close()
except Exception as e:
    print(f"Ошибка подключения: {e}")