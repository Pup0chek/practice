from starlette.testclient import TestClient
from practice.src.main import app

client = TestClient(app)


token_true = '12345'
token_false = '54321'

# @pytest.fixture
# def mock_dependencies(mocker):
#     mock_select_user = mocker.patch('database.actions.with_user.select_user')
#     mock_login = mocker.patch('database.actions.with_user.login')
#     mock_get_role_by_login = mocker.patch('database.actions.with_user.get_role_by_login')
#     mock_add_token = mocker.patch('database.actions.with_token.add_token')
#
#     return {
#         "select_user": mock_select_user,
#         "login": mock_login,
#         "get_role_by_login": mock_get_role_by_login,
#         "add_token": mock_add_token,
#     }

def test_get():
    response = client.get('/hello')
    assert response.json() == {"message": "Hello!"}

def test_true_post():
    data = {
        "key": "lol",
        "value": "lol",
        "token": f"{token_true}"
    }
    response = client.post("/create_record", json=data)
    assert response.json() == {"message": "lol"}



def test_false_post():
    data = {
        "key": "lol",
        "value": "lol",
        "token": f"{token_false}"
    }
    response = client.post("/create_record", json=data)
    assert response.json() == {"detail": "Unauthorized"}