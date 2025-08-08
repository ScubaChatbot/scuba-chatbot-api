from flask import Blueprint, request, jsonify
import logging
from prometheus_flask_exporter import Counter
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User



auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

# Prometheus metrics for authentication and registration
login_attempts_total = Counter('login_attempts_total', 'Total number of login attempts')
login_failed_total = Counter('login_failed_total', 'Total number of failed login attempts')
login_success_total = Counter('login_success_total', 'Total number of successful logins')
registration_attempts_total = Counter('registration_attempts_total', 'Total number of registration attempts')
registration_failed_total = Counter('registration_failed_total', 'Total number of failed registration attempts')
registration_success_total = Counter('registration_success_total', 'Total number of successful registrations')

@auth_bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    logger.info(f"Registration attempt for username: {username}")
    registration_attempts_total.inc()
    if not username or not password:
        logger.warning("Registration failed: missing username or password.")
        registration_failed_total.inc()
        return jsonify({'error': 'Username and password required'}), 400
    if User.query.filter_by(username=username).first():
        logger.warning(f"Registration failed: user '{username}' already exists.")
        registration_failed_total.inc()
        return jsonify({'error': 'User already exists'}), 409
    hashed_pw = generate_password_hash(password)
    user = User(username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    logger.info(f"User '{username}' registered successfully.")
    registration_success_total.inc()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    logger.info(f"Login attempt for username: {username}")
    login_attempts_total.inc()
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        logger.warning(f"Login failed for username: {username}")
        login_failed_total.inc()
        return jsonify({'error': 'Invalid credentials'}), 401
    from flask import current_app
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=2)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    logger.info(f"User '{username}' logged in successfully.")
    login_success_total.inc()
    return jsonify({'token': token}), 200

def token_required(f):
    from functools import wraps
    from flask import current_app

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        parts = auth_header.split()

        if len(parts) != 2 or parts[0] != 'Bearer':
            logger.warning("Token missing or invalid format in request.")
            return jsonify({'error': 'Token is missing or invalid format'}), 401

        token = parts[1]

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = db.session.get(User, data['user_id'])
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired.")
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated
