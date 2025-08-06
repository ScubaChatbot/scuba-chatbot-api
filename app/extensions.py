from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_cors import CORS

def init_cors(app):
    CORS(app, origins=["http://localhost:3001", "https://thankful-smoke-08a741103.1.azurestaticapps.net"], supports_credentials=True)
