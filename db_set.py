from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_connection_url import SQLALCHEMY_DATABASE_URL

# Создаем движок для подключения к базе данных
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Создаем фабрику сессий
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
