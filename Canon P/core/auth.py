from flask_login import LoginManager, current_user
from functools import wraps
from database.models import User

login_manager = LoginManager()
login_manager.login_view = 'main.index'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return {'error': 'Требуется авторизация'}, 401
        return f(*args, **kwargs)
    return decorated_function