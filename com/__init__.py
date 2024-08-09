from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from com.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from com.business import business_bp
    app.register_blueprint(business_bp, url_prefix='/business')

    from com.main import main_bp
    app.register_blueprint(main_bp)

    return app

from com import models
