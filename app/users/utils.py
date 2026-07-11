import os
import secrets
from PIL import Image
from flask import url_for, flash, current_app
from flask_mail import Message

from app import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(
        current_app.root_path,
        'static/profile_pics',
        picture_fn
    )

    img = Image.open(form_picture)

    # Crop to square
    width, height = img.size
    min_dim = min(width, height)

    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2

    img = img.crop((left, top, right, bottom))
    img = img.resize((125, 125))

    img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()

    reset_url = url_for(
        'users.reset_token',
        token=token,
        _external=True
    )

    msg = Message(
        'Password Reset Request',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )

    msg.body = f'''To reset your password, visit the following link:

{reset_url}

If you did not make this request, simply ignore this email and no changes will be made.
'''

    mail.send(msg)

    flash(
        'An email has been sent with instructions to reset your password.',
        'info'
    )