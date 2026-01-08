from datetime import datetime
from flask_login import UserMixin
from database.connection import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Профиль
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    pokecoins = db.Column(db.Integer, default=1000)
    battles_won = db.Column(db.Integer, default=0)
    pokemon_caught = db.Column(db.Integer, default=0)
    online_status = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'level': self.level,
            'pokecoins': self.pokecoins,
            'battles_won': self.battles_won,
            'pokemon_caught': self.pokemon_caught
        }

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    total_score = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='rating')
    
    def calculate_score(self):
        self.total_score = (self.user.battles_won * 10) + (self.user.pokemon_caught * 5) + (self.user.level * 100)
        return self.total_score

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    author = db.relationship('User', backref='news_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.strftime('%d.%m.%Y %H:%M'),
            'author': self.author.username if self.author else 'Система'
        }
    


