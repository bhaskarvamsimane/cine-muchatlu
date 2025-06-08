import os

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'

    # Database connection URI, fallback to local SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'

    # Disable Flask-SQLAlchemy event system to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
