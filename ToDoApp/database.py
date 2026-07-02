from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from pathlib import Path

# SQLite3
SQLALCHEMY_DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'todosapp.db'}"
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, pool_size=10, max_overflow=20)

# PostgresSQL
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://asus:asus@localhost/TodoApp"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autoflush=False, bind=engine)
class Base(DeclarativeBase):
    pass