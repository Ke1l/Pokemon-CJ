from datetime import datetime
from database.models import User, Rating, News, db

class UserService:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        if User.query.filter_by(username=username).first():
            raise ValueError('Имя пользователя уже занято')
        if User.query.filter_by(email=email).first():
            raise ValueError('Email уже зарегистрирован')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        rating = Rating(user_id=user.id)
        db.session.add(rating)
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate_user(email: str, password: str):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            user.online_status = True
            db.session.commit()
            return user
        return None
    
    @staticmethod
    def get_online_count():
        return User.query.filter_by(online_status=True).count()
    
    @staticmethod
    def get_today_users():
        today = datetime.utcnow().date()
        return User.query.filter(
            db.func.date(User.created_at) == today
        ).count()
    
    @staticmethod
    def get_leaderboard(limit: int = 10):
        ratings = Rating.query.join(User).order_by(
            Rating.total_score.desc()
        ).limit(limit).all()
        
        leaderboard = []
        for idx, rating in enumerate(ratings, 1):
            rating.calculate_score()
            leaderboard.append({
                'rank': idx,
                'username': rating.user.username,
                'level': rating.user.level,
                'score': rating.total_score,
                'battles': rating.user.battles_won,
                'pokemon': rating.user.pokemon_caught
            })
        
        return leaderboard

class NewsService:
    @staticmethod
    def get_latest_news(limit: int = 5):
        news_items = News.query.filter_by(
            is_published=True
        ).order_by(
            News.created_at.desc()
        ).limit(limit).all()
        
        return [item.to_dict() for item in news_items]