from starlette import status

from ..routers.admin import get_current_user, get_db
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get("/admin/todos")
    assert response.status_code == 200
    assert response.json() == [{'complete': False,
                                'title': 'Learn to Code',
                                'description': 'everyday learn to code',
                                'priority': 5,
                                'id': 1,
                                'owner_id': 1}]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todos/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id==1).first()
    assert model is None

def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todos/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}



