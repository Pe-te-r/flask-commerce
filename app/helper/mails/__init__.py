# 

from flask import render_template, current_app
from flask_mail import Message


def send_email(firstname, email, template='new', data=None):
    # Example dynamic content
    # message_body = "Welcome to our platform! We're glad to have you."

    # Create a message object
    msg = Message(
        # subject="Welcome to Our Company!",
        recipients=[email],
        sender=("phantom car rental's", "marketing@gmail.com"),
    )

    # Render the HTML template with dynamic content
    if template == "code":
        msg.subject = "Your verification code"
        msg.html = render_template(
            "code.html",  code=data
        )
    if template == "new":
        msg.subject = "Welcome to our platform"
        msg.html = render_template(
            "register.html", first_name=firstname
        )

    # mail.send(msg)
    with current_app.app_context():
        current_app.extensions["mail"].send(msg)
