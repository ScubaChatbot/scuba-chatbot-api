import pytest
from flask import Flask
from app.extensions import db
from app.models.user import User
from app.routes.auth import auth_bp
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'integration_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    db.init_app(app)
    app.register_blueprint(auth_bp)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_and_login(client):
    # Register
    resp = client.post('/users/register', json={'username': 'integration', 'password': 'pw'})
    assert resp.status_code == 201
    # Login
    resp = client.post('/users/login', json={'username': 'integration', 'password': 'pw'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'token' in data

def test_login_invalid_password(client):
    # Register
    client.post('/users/register', json={'username': 'integration2', 'password': 'pw'})
    # Login with wrong password
    resp = client.post('/users/login', json={'username': 'integration2', 'password': 'wrong'})
    assert resp.status_code == 401
    assert 'error' in resp.get_json()
