from database.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    # Profile picture filename
    profile_image = db.Column(
        db.String(255),
        nullable=False,
        default="default.png"
    )

    # Email Verification Status
    email_verified = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )