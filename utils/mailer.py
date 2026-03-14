import secrets
from datetime import datetime, timedelta

from flask import current_app

from model import PasswordResetToken, db


def send_registration_email(email: str, name: str) -> None:
    current_app.logger.info("Welcome email queued for %s <%s>", name, email)


def create_reset_token(user):
    token = secrets.token_urlsafe(32)
    reset = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=1),
    )
    db.session.add(reset)
    db.session.commit()
    return token


def get_valid_reset_token(token: str):
    reset = PasswordResetToken.query.filter_by(token=token, used=False).first()
    if not reset:
        return None
    if reset.expires_at < datetime.utcnow():
        return None
    return reset
