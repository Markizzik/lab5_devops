from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@example.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user_data = {
        "name": "New User",
        "email": "new.user@example.com"
    }
    response = client.post("/api/v1/user", json=new_user_data)
    assert response.status_code == 201
    user_id = response.json()
    assert isinstance(user_id, int)
    get_response = client.get("/api/v1/user", params={'email': new_user_data['email']})
    assert get_response.status_code == 200
    created_user = get_response.json()
    assert created_user['name'] == new_user_data['name']
    assert created_user['email'] == new_user_data['email']

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_user_data = {
        "name": "Duplicate User",
        "email": users[0]['email']
    }
    response = client.post("/api/v1/user", json=existing_user_data)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    new_user_data = {
        "name": "To Be Deleted",
        "email": "delete.me@example.com"
    }
    create_response = client.post("/api/v1/user", json=new_user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()
    delete_response = client.delete("/api/v1/user", params={'email': new_user_data['email']})
    assert delete_response.status_code == 204
    get_response = client.get("/api/v1/user", params={'email': new_user_data['email']})
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "User not found"}
