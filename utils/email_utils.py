from flask_mail import Message
from database.mail_config import mail


def send_verification_email(user_email, verification_link):

    msg = Message(
        subject="Verify Your Email",
        sender="pugalshanmugam0@gmail.com",
        recipients=[user_email]
    )

    msg.body = f"""
Hello,

Thank you for registering.

Please verify your email by clicking the link below:

{verification_link}

If you did not create this account, please ignore this email.

Regards,
Secure Authentication System
"""

    mail.send(msg)