from flask import current_app, render_template
from flask_mail import Message
from com import mail


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    with current_app.app_context():
        mail.send(msg)


def send_psw_reset_email(user):
    token = user.get_reset_psw_token()
    send_email(
        'Reset your password', sender=current_app.config['ADMINS'][0],
        recipients=[user.email], text_body=render_template('email/reset_password.txt',
                                                           user=user, token=token),
        html_body=render_template('email/reset_password.html',
                                  user=user, token=token)
               )
