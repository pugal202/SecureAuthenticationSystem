from flask import Flask
from database.db import db
from database.bcrypt_config import bcrypt
from database.mail_config import mail
from routes.auth import auth
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

app = Flask(__name__)

# Secret Key
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Pugal%401234@localhost:5432/secure_auth_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Upload Configuration
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

# Mail Configuration
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "True"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

# Initialize Extensions
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)

# Register Blueprint
app.register_blueprint(auth)

# Create Tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)