from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from pathlib import Path
from datetime import timedelta
import pytest
from ..database import Base
from ..main import app
from ..models import Todos, Users
from ..routers.auth import pwd_context, create_access_token   

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
    return {'username': 'phuctc', 'id': 1, 'user_role': 'admin', 'phone_number': '090909090'}

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)


TODO_DICT = {
        "title": "1st todo",
        "description": "Test 01",
        "priority": 5,
        "complete": False,
        "owner_id": 1,
        }

TODO_DICT_NEW = {
        "title": "2nd todo!",
        "description": "Test 02",
        "priority": 4,
        "complete": False,
        "owner_id": 1,
        }

TODO_DICT_UPDATE = {
        "title": "03 todo!",
        "description": "Test 03",
        "priority": 3,
        "complete": False,
        "owner_id": 1,
        }

USER_DICT = {
        "id": 1,
        "username": "phuctc",
        "email": "phuctc@email.com",
        "first_name": "Phuc",
        "last_name": "Tran",
        "hashed_password": pwd_context.hash("Happy@111"),
        # "hashed_password": "Happy@111",
        "role": "admin",
        "phone_number": "0909090909"       
        }

@pytest.fixture
def pytest_clear_todo():
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


# @pytest.fixture(scope="module")
@pytest.fixture
def pytest_create_todo():
    todo = Todos(**TODO_DICT)
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture()
def pytest_create_user():
    user = Users(**USER_DICT)
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()   

TOKEN = create_access_token(
    USER_DICT.get('username'), 
    USER_DICT.get('id'), 
    USER_DICT.get('role'), 
    timedelta(days=1)
    )

def compare_user_object_and_dict(user_obj, user_dict):
    if user_obj.username != user_dict.get("username"):
        return False
    if user_obj.email != user_dict.get("email"):
        return False    
    if user_obj.role != user_dict.get("role"):
        return False
    if user_obj.phone_number != user_dict.get("phone_number"):
        return False
    return True

def get_todo_by_id_from_db(id):
    db = TestingSessionLocal()
    todo_model = db.query(Todos).filter(Todos.id==id).first()
    return todo_model

def get_user_by_username_from_db(username):
    db = TestingSessionLocal()
    user_model = db.query(Users).filter(Users.username==username).first()
    return user_model

def compare_todo_object_and_dict(todo_obj, todo_dict):
    if todo_obj.title != todo_dict.get("title"):
        return False
    if todo_obj.description != todo_dict.get("description"):
        return False    
    if todo_obj.priority != todo_dict.get("priority"):
        return False
    if todo_obj.complete != todo_dict.get("complete"):
        return False
    return True

