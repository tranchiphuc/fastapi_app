from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from pathlib import Path
import pytest
from ..database import Base
from ..main import app
from ..models import Todos, Users
from ..routers.auth import pwd_context

# SQLite3
SQLALCHEMY_DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'test.db'}"
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool
)
# PostgresSQL
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://asus:asus@localhost/TodoApp"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'codingwithrobytest', 'id': 1, 'user_role': 'admin'}

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)


TODO_DICT = {"title": "Learn to code!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
        "owner_id": 1
        }

USER_DICT = {
        "username": "phuctc",
        "email": "phuctc@email.com",
        "first_name": "Phuc",
        "last_name": "Tran",
        "hashed_password": pwd_context.hash("Happy@111"),
        "role": "admin",
        "phone_number": "0909090909"       
        }

@pytest.fixture
def create_todo():
    todo = Todos(**TODO_DICT)
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def create_user():
    user = Users(**USER_DICT)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()    


