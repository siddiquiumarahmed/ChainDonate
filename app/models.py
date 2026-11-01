from datetime import datetime

from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="donor")

    donations = db.relationship("Donation", backref="user", lazy=True)


class Charity(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text)

    category = db.Column(db.String(100))

    donations = db.relationship("Donation", backref="charity", lazy=True)


class Donation(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float, nullable=False)

    donation_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    transaction_hash = db.Column(db.String(255))

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    charity_id = db.Column(
        db.Integer,
        db.ForeignKey("charity.id"),
        nullable=False
    )


from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))