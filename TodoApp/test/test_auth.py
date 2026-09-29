from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from ..routers.auth import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_db,
)
from .utils import *

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, "admin", db)
    assert authenticate_user is not None
    assert authenticated_user.username == test_user.username

    nonexistent_user = authenticate_user("a","admin", db)
    assert nonexistent_user is False

    wrong_password_user = authenticate_user(test_user.username, "admin1", db)
    assert wrong_password_user is False

@pytest.mark.asyncio
async def test_create_access_token(test_user):
    username = 'test_user'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user():

    encode = {'sub': 'test_user', 'role': 'admin', 'id': 1}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {'username': 'test_user', 'user_role': 'admin', 'user_id': 1}


@pytest.mark.asyncio
async def test_verify_token_missing_payload():

    encode = {'sub': 'test_user', 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate credentials'