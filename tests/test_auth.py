import pytest
from flask import Flask
from app.routes.auth import auth_bp
from app.models.user import User
from werkzeug.security import generate_password_hash
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret'
    app.register_blueprint(auth_bp)
    app.testing = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_success(client):
    with client.application.app_context():
        with patch('app.models.user.User.query') as mock_query, \
             patch('app.extensions.db.session') as mock_session:
            mock_query.filter_by.return_value.first.return_value = None
            response = client.post('/users/register', json={'username': 'test', 'password': 'pw'})
            assert response.status_code == 201
            assert response.get_json()['message'] == 'User registered successfully'
            assert mock_session.add.called
            assert mock_session.commit.called

def test_register_missing_fields(client):
    response = client.post('/users/register', json={'username': 'test'})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_register_user_exists(client):
    with client.application.app_context():
        with patch('app.models.user.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = User(username='test', password='pw')
            response = client.post('/users/register', json={'username': 'test', 'password': 'pw'})
            assert response.status_code == 409
            assert 'error' in response.get_json()

def test_login_success(client):
    with client.application.app_context():
        hashed_pw = generate_password_hash('pw')
        user = User(id=1, username='test', password=hashed_pw)
        with patch('jwt.encode', return_value='token'), \
             patch('app.models.user.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = user
            response = client.post('/users/login', json={'username': 'test', 'password': 'pw'})
            assert response.status_code == 200
            assert 'token' in response.get_json()

def test_login_invalid_credentials(client):
    with client.application.app_context():
        with patch('app.models.user.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = None
            response = client.post('/users/login', json={'username': 'test', 'password': 'wrong'})
            assert response.status_code == 401
            assert 'error' in response.get_json()

def test_token_required_missing_token(client):
    # Create a dummy protected route for testing
    from app.routes.auth import token_required
    from flask import jsonify

    @client.application.route('/protected')
    @token_required
    def protected(current_user):
        return jsonify({'ok': True})

    response = client.get('/protected')
    assert response.status_code == 401
    assert 'error' in response.get_json()

def test_token_required_invalid_token(client):
    import jwt
    from app.routes.auth import token_required
    from flask import jsonify

    @client.application.route('/protected2')
    @token_required
    def protected2(current_user):
        return jsonify({'ok': True})

    headers = {'Authorization': 'Bearer invalidtoken'}
    with patch('jwt.decode', side_effect=jwt.InvalidTokenError('Invalid')):
        response = client.get('/protected2', headers=headers)
        assert response.status_code == 401
        assert 'error' in response.get_json()
