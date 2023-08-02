import pytest
import requests as requests
from unittest.mock import Mock

@pytest.fixture
def api_response():
  return Mock()




def test_index_endpoint():
    response = requests.get('http://127.0.0.1:5000/')
    assert response.status_code == 200

def test_index_endpoint_post_with_invalid_input():
    response = requests.post('http://127.0.0.1:5000/',{'n': '-5'})
    assert response.status_code == 404

def test_index_endpoint_post_with_valid_input():
    response = requests.post('http://127.0.0.1:5000/', {'n': '5'})
    assert response.status_code == 200
