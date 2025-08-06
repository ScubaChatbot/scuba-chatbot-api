import pytest
from flask import Flask
from app import extensions
from app.models.user import User
from app.routes.auth import auth_bp
from app.routes.chat import create_chat_bp
from werkzeug.security import generate_password_hash
import os
import tempfile

@pytest.fixture(scope="module")
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'integration_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    extensions.db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(create_chat_bp())
    with app.app_context():
        extensions.db.create_all()
        yield app
        extensions.db.session.remove()
        extensions.db.drop_all()
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_login_chat_flow(client):
    # Register
    resp = client.post('/users/register', json={'username': 'integration', 'password': 'pw'})
    assert resp.status_code == 201
    # Login
    resp = client.post('/users/login', json={'username': 'integration', 'password': 'pw'})
    assert resp.status_code == 200
    token = resp.get_json()['token']
    # Patch generate_rag_answer to avoid real LLM calls
    from unittest.mock import patch
    dummy_response = {"messages": [{"role": "assistant", "content": "Echo: ¿Cuál es el horario?"}]}
    headers = {'Authorization': f'Bearer {token}'}
    with patch('app.services.chat.generate_rag_answer', return_value=dummy_response):
        resp = client.post('/chat', json={'message': '¿Cuál es el horario?'}, headers=headers)
        assert resp.status_code == 200
        assert 'response' in resp.get_json()
        assert isinstance(resp.get_json()['response'], str)

def test_chat_requires_auth(client):
    resp = client.post('/chat', json={'message': 'Hola'})
    assert resp.status_code == 401
    assert 'error' in resp.get_json()

def test_invalid_login(client):
    resp = client.post('/users/login', json={'username': 'noexiste', 'password': 'bad'})
    assert resp.status_code == 401
    assert 'error' in resp.get_json()
