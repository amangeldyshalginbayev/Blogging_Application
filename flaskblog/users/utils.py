import os
import secrets
import re
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture, directory='static/profile_pics'):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, directory, picture_fn)

    i = Image.open(form_picture)

    # Here we need to resize image, if we are using it for profile_picture.
    # If we are using it for post image, no need to resize the image.
    if directory == 'static/profile_pics':
        output_size = (125, 125)
        i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn


def remove_picture(picture_name, directory='static/profile_pics'):
    picture_path = os.path.join(current_app.root_path, directory, picture_name)
    if os.path.isfile(picture_path):
        os.remove(picture_path)


def send_reset_email(user):
    token = user.get_token()
    msg = Message('Password Reset Request. Do not reply to this email',
                  recipients=[user.email])
    msg.body = f'''Hi! To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_activation_email(user):
    token = user.get_token()
    msg = Message('Account activation. Do not reply to this email',
                  recipients=[user.email])
    msg.body = f'''Hi! Please visit the following link to activate your account:
{url_for('users.activate_account', token=token, _external=True)}

If you did not register an account in our service then simply ignore this email.
'''
    mail.send(msg)


def is_password_valid(password):
    is_valid = False
    uppercase = r"[A-Z]"
    lowercase = r"[a-z]"
    number = r"[0-9]"
    non_alphanumeric = r"\W"

    for pattern in (uppercase, lowercase, number, non_alphanumeric):
        if not re.search(pattern, password):
            break
    else:
        is_valid = True
    return is_valid


def is_mobile_phone_valid(number):
    is_valid = False
    pattern = r"^\+[1-9]\d{1,14}$"
    if re.search(pattern, number):
        is_valid = True
    return is_valid
