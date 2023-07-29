import json
import pytest
from app import app, db, Fibonacci

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.drop_all()

def test_generate_fibonacci():
    from app import generate_fibonacci

    assert generate_fibonacci(1) == [0]
    assert generate_fibonacci(2) == [0, 1]
    assert generate_fibonacci(5) == [0, 1, 1, 2, 3]
    assert generate_fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Fibonacci Number Generator' in response.data
    assert b'Enter the value of n:' in response.data

def test_fibonacci_list_page(client):
    response = client.post('/', data={'n': 10})
    assert response.status_code == 302

    response = client.get('/fibonacci_list')
    assert response.status_code == 200
    assert b'Fibonacci Numbers' in response.data
    assert b'0,1,1,2,3,5,8,13,21,34' in response.data