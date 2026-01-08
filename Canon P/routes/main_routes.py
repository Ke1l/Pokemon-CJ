from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from services.user_service import UserService, NewsService
from core.auth import login_required as auth_login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    if 'login' in request.form:
        return handle_login()
    elif 'register' in request.form:
        return handle_register()
    
    return render_template('index.html')

def handle_login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = UserService.authenticate_user(email, password)
    if user:
        login_user(user)
        if request.headers.get('HX-Request'):
            return '''
            <div class="alert success" id="auth-alert">
                ✓ Успешный вход!
            </div>
            <script>
                setTimeout(() => {
                    location.reload();
                }, 1000);
            </script>
            '''
        return redirect(url_for('main.index'))
    
    if request.headers.get('HX-Request'):
        return '''
        <div class="alert error" id="auth-alert">
            ✗ Неверный email или пароль
        </div>
        '''
    flash('Неверный email или пароль', 'error')
    return redirect(url_for('main.index'))

def handle_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        user = UserService.create_user(username, email, password)
        login_user(user)
        if request.headers.get('HX-Request'):
            return '''
            <div class="alert success" id="auth-alert">
                ✓ Регистрация успешна! Добро пожаловать!
            </div>
            <script>
                setTimeout(() => {
                    location.reload();
                }, 1000);
            </script>
            '''
        return redirect(url_for('main.index'))
    except ValueError as e:
        if request.headers.get('HX-Request'):
            return f'''
            <div class="alert error" id="auth-alert">
                ✗ {str(e)}
            </div>
            '''
        flash(str(e), 'error')
        return redirect(url_for('main.index'))

@main_bp.route('/logout')
@auth_login_required
def logout():
    current_user.online_status = False
    from database.connection import db
    db.session.commit()
    logout_user()
    
    if request.headers.get('HX-Request'):
        return '''
        <div class="alert info" id="auth-alert">
            Вы вышли из системы
        </div>
        <script>
            setTimeout(() => {
                location.reload();
            }, 1000);
        </script>
        '''
    return redirect(url_for('main.index'))

@main_bp.route('/news')
def get_news():
    news_items = NewsService.get_latest_news()
    
    if not news_items:
        return '''
        <div class="news-item">
            <div class="news-title">Новостей пока нет</div>
            <div class="news-content">Скоро появятся обновления!</div>
        </div>
        '''
    
    html = ''
    for news in news_items:
        html += f'''
        <div class="news-item">
            <div class="news-header">
                <div class="news-title">{news['title']}</div>
                <div class="news-date">{news['created_at']}</div>
            </div>
            <div class="news-content">{news['content']}</div>
            <div class="news-author">Автор: {news['author']}</div>
        </div>
        '''
    
    return html