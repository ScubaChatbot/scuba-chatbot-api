from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_cors import CORS

def init_cors(app):
    CORS(app, origins=["http://localhost:3001"], supports_credentials=True)
