from flask import Flask
from config import config
from database.connection import init_db
from core.auth import login_manager
from routes.main_routes import main_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_db(app)
    login_manager.init_app(app)
    app.register_blueprint(main_bp)
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, port=5000)