from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app
)

from models.user import User
from database.db import db
from database.bcrypt_config import bcrypt
from utils.validators import validate_password
from utils.token_utils import generate_token, verify_token
from utils.email_utils import send_verification_email
from werkzeug.utils import secure_filename
import os

auth = Blueprint("auth", __name__)


# ---------------- HOME ----------------
@auth.route("/")
def home():
    return redirect(url_for("auth.login"))


# ---------------- REGISTER ----------------
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Confirm Password
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("auth.register"))

        # Password Validation
        error = validate_password(password)

        if error:
            flash(error, "danger")
            return redirect(url_for("auth.register"))

        # Duplicate Email Check
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("auth.register"))

        # Hash Password
        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        # Save User
        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        # ==========================
        # EMAIL VERIFICATION
        # ==========================

        # Uncomment these lines after fixing Flask-Mail on Render

        # token = generate_token(user.email)

        # verification_link = url_for(
        #     "auth.verify_email",
        #     token=token,
        #     _external=True
        # )

        # send_verification_email(
        #     user.email,
        #     verification_link
        # )

        flash(
            "Registration Successful!",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ---------------- VERIFY EMAIL ----------------
@auth.route("/verify-email/<token>")
def verify_email(token):

    email = verify_token(token)

    if not email:
        flash(
            "Verification link is invalid or expired!",
            "danger"
        )
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for("auth.login"))

    if user.email_verified:
        flash("Email already verified!", "info")
        return redirect(url_for("auth.login"))

    user.email_verified = True

    db.session.commit()

    flash(
        "Email verified successfully! You can now login.",
        "success"
    )

    return redirect(url_for("auth.login"))


# ---------------- LOGIN ----------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        # Temporarily disable email verification
           # if user and not user.email_verified:
        #     flash(
        #         "Please verify your email before logging in.",
        #         "warning"
        #     )
        #     return redirect(url_for("auth.login"))

        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id
            session["username"] = user.username

            flash("Login Successful!", "success")
            return redirect(url_for("auth.dashboard"))

        flash("Invalid Email or Password!", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@auth.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    return render_template(
        "dashboard.html",
        user=user
    )


# ---------------- EDIT PROFILE ----------------
@auth.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        profile_image = request.files.get("profile_image")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user and existing_user.id != user.id:
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.edit_profile"))

        user.username = username
        user.email = email

        if profile_image and profile_image.filename != "":

            filename = secure_filename(profile_image.filename)

            upload_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )

            profile_image.save(upload_path)

            user.profile_image = filename

        db.session.commit()

        session["username"] = username

        flash("Profile updated successfully!", "success")

        return redirect(url_for("auth.dashboard"))

    return render_template(
        "edit_profile.html",
        user=user
    )


# ---------------- CHANGE PASSWORD ----------------
@auth.route("/change-password", methods=["GET", "POST"])
def change_password():

    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if not bcrypt.check_password_hash(
            user.password,
            current_password
        ):
            flash("Current password is incorrect!", "danger")
            return redirect(url_for("auth.change_password"))

        if new_password != confirm_password:
            flash("New passwords do not match!", "danger")
            return redirect(url_for("auth.change_password"))

        error = validate_password(new_password)

        if error:
            flash(error, "danger")
            return redirect(url_for("auth.change_password"))

        user.password = bcrypt.generate_password_hash(
            new_password
        ).decode("utf-8")

        db.session.commit()

        flash(
            "Password changed successfully!",
            "success"
        )

        return redirect(url_for("auth.dashboard"))

    return render_template("change_password.html")

   # ---------------- FORGOT PASSWORD ----------------
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No account found with this email!", "danger")
            return redirect(url_for("auth.forgot_password"))

        # ===========================================
        # EMAIL RESET TEMPORARILY DISABLED
        # Uncomment after fixing Flask-Mail
        # ===========================================

        # token = generate_token(user.email)

        # reset_link = url_for(
        #     "auth.reset_password",
        #     token=token,
        #     _external=True
        # )

        # send_verification_email(
        #     user.email,
        #     reset_link
        # )

        flash(
            "Password reset feature is temporarily disabled.",
            "warning"
        )

        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html")


# ---------------- RESET PASSWORD ----------------
@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    email = verify_token(token)

    if not email:
        flash("Reset link is invalid or expired!", "danger")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":

        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(
                url_for("auth.reset_password", token=token)
            )

        error = validate_password(password)

        if error:
            flash(error, "danger")
            return redirect(
                url_for("auth.reset_password", token=token)
            )

        user.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        db.session.commit()

        flash(
            "Password reset successfully! Please login.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "reset_password.html",
        token=token
    )


# ---------------- LOGOUT ----------------
@auth.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully!",
        "success"
    )

    return redirect(url_for("auth.login")) 