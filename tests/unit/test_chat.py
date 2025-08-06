import pytest
from flask import Flask
from unittest.mock import patch
import jwt

@pytest.fixture
def app():
    from app.routes.auth import token_required
    from app.routes.chat import create_chat_bp
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret'
    chat_bp = create_chat_bp()
    app.register_blueprint(chat_bp)
    app.testing = True
    yield app

@pytest.fixture
def app_authed():
    def fake_token_required(f):
        def wrapper(*args, **kwargs):
            return f("dummy_user", *args, **kwargs)
        return wrapper

    with patch("app.routes.auth.token_required", fake_token_required):
        from app.routes.chat import create_chat_bp
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test_secret'
        chat_bp = create_chat_bp()
        app.register_blueprint(chat_bp)
        app.testing = True
        yield app

@pytest.fixture
def client(app):
    with app.app_context():
        yield app.test_client()

@pytest.fixture
def client_authed(app_authed):
    with app_authed.app_context():
        yield app_authed.test_client()

def make_token():
    # Return a dummy token for testing
    return "dummytoken"

def auth_header(token=None):
    return {'Authorization': f'Bearer {token or make_token()}'}

def test_chat_success(client_authed):
    with patch('app.routes.chat.generate_rag_answer') as mock_rag:
        mock_rag.return_value = {"messages": [{"role": "assistant", "content": "Hello, diver!"}]}
        response = client_authed.post('/chat', json={'message': 'Hi'}, headers=auth_header())
        assert response.status_code == 200
        assert response.get_json()['response'] == "Hello, diver!"

def test_chat_missing_token(client):
    import jwt
    response = client.post('/chat', json={'message': 'Hi'})
    print("Missing token response:", response.status_code, response.data)
    assert response.status_code == 401
    assert 'error' in response.get_json()

def test_chat_invalid_token(client):
    import jwt
    with patch('jwt.decode', side_effect=jwt.InvalidTokenError('Invalid')):
        headers = auth_header('invalidtoken')
        response = client.post('/chat', json={'message': 'Hi'}, headers=headers)
        print("Invalid token response:", response.status_code, response.data)
        assert response.status_code == 401
        assert 'error' in response.get_json()

def test_chat_missing_message(client_authed):
    with patch('app.routes.chat.generate_rag_answer') as mock_rag:
        mock_rag.return_value = {"messages": [{"role": "assistant", "content": "Missing message"}]}
        response = client_authed.post('/chat', json={}, headers=auth_header())
        assert response.status_code == 200
        assert response.get_json()['response'] == "Missing message"

def test_chat_unknown_product(client_authed):
    with patch('app.routes.chat.generate_rag_answer') as mock_rag:
        mock_rag.return_value = {"messages": [{"role": "assistant", "content": "No conozco ese producto."}]}
        response = client_authed.post('/chat', json={'message': 'What about AtlantisX?'}, headers=auth_header())
        assert response.status_code == 200
        assert response.get_json()['response'] == "No conozco ese producto."

def test_chat_llm_error(client_authed):
    with patch('app.routes.chat.generate_rag_answer', return_value={"messages": [{"role": "assistant", "content": "Lo siento, ocurrió un error al procesar tu consulta."}]}):
        response = client_authed.post('/chat', json={'message': 'Trigger error'}, headers=auth_header())
        assert response.status_code == 200
        assert "error" in response.get_json()['response'] or "Lo siento" in response.get_json()['response']
