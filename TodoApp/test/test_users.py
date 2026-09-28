from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status
from ..routers.auth import bcrypt_context


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_current_user(test_user):
    response = client.get("/Users/current_user_info")
    assert response.status_code == 200
    assert response.json()['username'] == 'sachin'
    #cant test password


def test_update_current_user_password(test_user):
    response = client.put("/Users/update_current_user_password",
                          json={"password": "admin",
                                "new_password": "admin1"
                                })
    assert response.status_code == 204


def test_update_current_user_wrong_password(test_user):
    response = client.put("/Users/update_current_user_password",
                          json={"password": "wrong password",
                                "new_password": "admin1"
                                })
    assert response.status_code == 401
    assert response.json() == {'detail': 'User not found'}


def test_update_phone_number(test_user):
    response = client.put("/Users/update_phone_number",
                          json={"new_phone_number": "12345",})
    assert response.status_code == 204
