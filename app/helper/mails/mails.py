from flask import render_template
from flask_mail import Message
from app import mail


def send_email(subject, recipients, template_name, **kwargs):
    """
    Send an email using Flask-Mail.

    :param subject: Subject of the email
    :param recipients: List of recipient email addresses
    :param template_name: Template file to use
    :param kwargs: Data to pass to the template
    """

    try:
        print('ZERO')
        html_body = render_template(
            f"{template_name}.html", **kwargs
        )
        print('one')
        msg = Message(subject, recipients=recipients, html=html_body)
        print('two')
        mail.send(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

    # mail.send(msg)
    print('three')
