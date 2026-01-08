from app import create_app
from database.connection import db
from database.models import User, Rating, News
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Add test users if they don't exist
    test_users = [
        ('Ash', 'ash@pokemon.game', 25, 10500, 120, 85),
        ('Misty', 'misty@pokemon.game', 22, 8500, 80, 65),
        ('Brock', 'brock@pokemon.game', 24, 9200, 95, 75),
        ('Gary', 'gary@pokemon.game', 26, 11000, 130, 90),
        ('Jessie', 'jessie@teamrocket.game', 20, 5500, 65, 45),
        ('James', 'james@teamrocket.game', 19, 5000, 60, 40),
        ('Red', 'red@pokemon.game', 30, 20000, 200, 150),
        ('Blue', 'blue@pokemon.game', 28, 18000, 180, 140),
    ]
    
    for username, email, level, coins, battles, pokemon in test_users:
        if not User.query.filter_by(username=username).first():
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash('password123'),
                level=level,
                pokecoins=coins,
                battles_won=battles,
                pokemon_caught=pokemon,
                online_status=True,
                created_at=datetime.utcnow() - timedelta(days=5)
            )
            db.session.add(user)
            db.session.commit()
            
            rating = Rating(user_id=user.id)
            rating.calculate_score()
            db.session.add(rating)
    
    # Add news
    admin = User.query.filter_by(username='admin').first()
    
    news_items = [
        ('Обновление системы боев', 'Мы запустили новую систему боев с улучшенной механикой и балансом. Теперь каждый бой стал еще более захватывающим!'),
        ('Турнир выходного дня', 'В эту субботу состоится турнир с призовым фондом 10,000 покемонет. Регистрация открыта до пятницы.'),
        ('Новые покемоны в игре', 'Добавлены редкие покемоны: Mewtwo, Charizard, Blastoise. Ищите их в специальных локациях.'),
        ('Магазин обновлен', 'В магазине появились новые предметы: Ультра шары, Зелья лечения, TM-ки различных типов.'),
        ('Событие: Двойной опыт', 'В эти выходные действует событие "Двойной опыт". Успейте прокачаться быстрее!'),
        ('Новая локация: Пещера Лунного Света', 'Открыта новая локация для исследования с уникальными покемонами и заданиями.'),
        ('Балансные изменения', 'Внесены корректировки в баланс некоторых типов покемонов для более честных боев.'),
        ('Система друзей', 'Теперь вы можете добавлять друзей, общаться и проводить тренировочные бои.'),
    ]
    
    for i, (title, content) in enumerate(news_items):
        if not News.query.filter_by(title=title).first():
            news = News(
                title=title,
                content=content,
                author_id=admin.id,
                created_at=datetime.utcnow() - timedelta(days=len(news_items) - i)
            )
            db.session.add(news)
    
    db.session.commit()
    
    print("✅ Демо данные добавлены!")
    print(f"📊 Всего пользователей: {User.query.count()}")
    print(f"📰 Всего новостей: {News.query.count()}")