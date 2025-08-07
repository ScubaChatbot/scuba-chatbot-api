import os
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    from app.extensions import db, init_cors
    db.init_app(app)
    init_cors(app)

    from app.routes.chat import create_chat_bp
    app.register_blueprint(create_chat_bp())

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.health import health_bp
    app.register_blueprint(health_bp)

    with app.app_context():
        db.create_all()

    # Initialize Prometheus metrics
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        PrometheusMetrics(app, path="/metrics")
        
    return app
