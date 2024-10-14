import jwt
from com import db, bcrypt, login_manager
from flask_login import UserMixin
from flask import current_app
from time import time


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    has_business_page = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_login_psw(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def get_reset_psw_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_psw_token(token):
        try:
            id = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)


class Item(db.Model):
    # ==Item is User's business==
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    url_friendly_name = db.Column(db.String(length=30), nullable=False, unique=True)
    category = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(length=1024))
    phone = db.Column(db.String())
    address = db.Column(db.String())
    web_page = db.Column(db.String())
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    owner_name = db.Column(db.String(length=60), nullable=False)

    def __repr__(self):
        return f'Item {self.name}'

