# 🔐 Secure Authentication System

A secure and feature-rich authentication system built using **Flask**, **PostgreSQL**, and **SQLAlchemy**. This project demonstrates modern authentication techniques, secure password handling, email verification, password reset functionality, profile management, and image upload.

---

## 🚀 Features

- ✅ User Registration
- ✅ User Login & Logout
- ✅ Secure Password Hashing (Bcrypt)
- ✅ Strong Password Validation
- ✅ Email Verification
- ✅ Forgot Password
- ✅ Secure Password Reset
- ✅ Profile Management
- ✅ Profile Picture Upload
- ✅ Session Management
- ✅ PostgreSQL Database Integration
- ✅ Flask-Mail Integration
- ✅ Environment Variable Configuration (.env)

---

## 🛠️ Tech Stack

### Backend
- Python 3
- Flask
- SQLAlchemy
- Flask-Bcrypt
- Flask-Mail

### Database
- PostgreSQL

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Jinja2

### Security
- Bcrypt Password Hashing
- Email Verification
- Password Reset Tokens
- Session Authentication
- Environment Variables (.env)

---

## 📂 Project Structure

```text
SecureAuthenticationSystem/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
├── models/
├── routes/
├── static/
│   ├── css/
│   └── uploads/
├── templates/
├── utils/
└── .env
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/pugal202/SecureAuthenticationSystem.git
```

### Navigate

```bash
cd SecureAuthenticationSystem
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file.

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=secure_auth_db
DB_USER=postgres
DB_PASSWORD=your_password

SECRET_KEY=your_secret_key

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

### Run

```bash
python app.py
```

---

## 📸 Screenshots

### Register Page

(Add Screenshot)

### Login Page

(Add Screenshot)

### Dashboard

(Add Screenshot)

### Edit Profile

(Add Screenshot)

---

## 🔒 Security Features

- Password Hashing using Bcrypt
- Strong Password Validation
- Email Verification
- Secure Password Reset
- Session-Based Authentication
- Environment Variable Protection

---

## 👨‍💻 Author

**Pugal**

GitHub:
https://github.com/pugal202

---

## ⭐ If you like this project

Give this repository a ⭐ on GitHub.
