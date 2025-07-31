from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 409
    hashed_pw = generate_password_hash(password)
    user = User(username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    from flask import current_app
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=2)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200

def token_required(f):
    from functools import wraps
    from flask import current_app

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != 'Bearer':
            return jsonify({'error': 'Token is missing or invalid format'}), 401

        token = parts[1]

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated
