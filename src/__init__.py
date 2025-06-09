from flask import Flask
from src.config import Config

def create_app(config_class=Config):
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')
    
    app.config.from_object(config_class)

    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app