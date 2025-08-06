import pytest
from flask import Flask
from app.routes.chat import create_chat_bp
from app.extensions import db
from unittest.mock import patch

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    db.init_app(app)
    # Registrar ambos blueprints para que existan los endpoints de auth y chat
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(create_chat_bp())
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_chat_protected_and_mocked(client):
    # Verifica que /chat requiere auth
    resp = client.post('/chat', json={'message': 'Hola'})
    assert resp.status_code == 401
    assert 'error' in resp.get_json()

    # Mockea generate_rag_answer en el namespace correcto y prueba respuesta básica con token dummy
    with patch('app.routes.chat.generate_rag_answer') as mock_rag:
        mock_rag.return_value = {"messages": [{"role": "assistant", "content": "Mocked!"}]}
        # Forzamos bypass del decorador usando test_request_context y manualmente
        app = client.application
        with app.test_request_context('/chat', method='POST', json={'message': 'Hola'}):
            from app.routes.chat import handle_chat_request
            resp = handle_chat_request(current_user='dummy')
            assert resp.status_code == 200
            data = resp.get_json()
            assert data['response'] == 'Mocked!'

def test_chat_missing_auth(client):
    resp = client.post('/chat', json={'message': 'Hola'})
    assert resp.status_code == 401
    assert 'error' in resp.get_json()
