from os import environ
from dotenv import load_dotenv

# Загрузка параметров из .env файла
load_dotenv()

# Формируем строку подключения к базе данных
SQLALCHEMY_DATABASE_URL = "mysql://{user}@{host}/{db_name}".format(
    user=environ.get('DB_USER', 'root'),          # Пользователь (по умолчанию 'root')
    host=environ.get('DB_HOST', 'localhost'),     # Хост (по умолчанию 'localhost')
    db_name=environ.get('DB_NAME', 'test_db')     # Имя базы данных (по умолчанию 'test_db')
)
