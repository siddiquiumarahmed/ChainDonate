from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from . import models
    from app.models import User

    with app.app_context():
        db.create_all()

        # Create default admin account if it doesn't exist
        admin = User.query.filter_by(email="admin@gmail.com").first()

        if not admin:
            admin = User(
                name="Administrator",
                email="admin@gmail.com",
                password_hash=bcrypt.generate_password_hash(
                    "admin@123"
                ).decode("utf-8"),
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()

    from app.routes import main
    app.register_blueprint(main)

    return app