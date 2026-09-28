


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from sqlalchemy.testing.pickleable import User

from ..routers.users import bcrypt_context
from ..models import Todo, Users

from ..database import Base
from ..main import app
import pytest


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False},
                       poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'sachin',
            'user_id': 1,
            'user_role': 'admin'}


client = TestClient(app)
@pytest.fixture
def test_todo():
    todo = Todo(
        title="Learn to Code",
        description="everyday learn to code",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="sachin",
        email="sachin619@gmail.com",
        hashed_password=bcrypt_context.hash("admin"),
        role="admin",
        first_name="sachin",
        last_name="M",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()