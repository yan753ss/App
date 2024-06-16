from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        from . import views, models, auth, log_parser
        app.register_blueprint(views.views, url_prefix='/')
        app.register_blueprint(auth.auth, url_prefix='/auth')
        db.create_all()
    
    return app
