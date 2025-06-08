from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load config from instance/config.py
    app.config.from_pyfile('config.py')

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    # Import and register blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    csrf.init_app(app)

    from app import routes
    app.register_blueprint(routes.main)

    return app
