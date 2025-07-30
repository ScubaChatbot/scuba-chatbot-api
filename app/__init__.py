from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    from app.extensions import db
    db.init_app(app)

    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app