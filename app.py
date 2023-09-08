"""This module handles the web application routes and views."""
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from models import db
from views import main_blueprint


login_manager = LoginManager()



def create_app():
    """Flaskアプリケーションを作成するための関数"""
    app = Flask(__name__)  # pylint: disable=redefined-outer-name
    migrate = Migrate(app, db)

    app.debug = True

    app.secret_key = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login_page'
    login_manager.session_protection = "strong"

    
    app.register_blueprint(main_blueprint)
      
    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

app = create_app() 






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
