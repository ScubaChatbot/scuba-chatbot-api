import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'default_key_for_dev')
SQLALCHEMY_DATABASE_URI = 'sqlite:///scuba_chatbot.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
