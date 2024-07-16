import logging

from typing import Any
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import F

from common.dependencies import connect_redis
from . import exceptions
from .models import BaseUser
from .types import Email, Password

logger = logging.getLogger("backend")


def set_verification_code_to_redis(*, email: Email) -> str:
    verification_code = (uuid4().hex)[0:7] # Example => 'd33b1ff'
    redis_connection = connect_redis()
    redis_connection.set(
        name=verification_code, value=email,
        ex=int(settings.VERIFICATION_EMAIL_EXPIRY_SEC)
    ) # Example => key: 'd33b1ff', value: user@example.com
    return verification_code


def user_register(*, email: Email, password: Password) -> BaseUser:
    try:
        user = BaseUser.objects.create_user(email=email, password=password)
        verification_code = set_verification_code_to_redis(email=email)
        # TODO: Sending verification_code to user email
        return user
    except ValidationError:
        raise exceptions.UserAlreadyExists


def user_change_password(
        *, user: BaseUser, old_password: Password, new_password: Password
) -> None:
    if not user.check_password(old_password):
        raise exceptions.PasswordIsWrong
    user.set_password(new_password)
    user.save(update_fields=['password'])


def user_verify_account(*, verification_code: str) -> None:
    redis_connection = connect_redis()
    user_email: Any = redis_connection.get(verification_code)
    if user_email:
        user = BaseUser.objects.get(email=user_email.decode("ascii"))
        if user.is_active:
            raise exceptions.UserAlreadyVerified
        user.is_active = ~F("is_active")
        user.save(update_fields=["is_active"])
    else:
        raise exceptions.InvalidVerificationCode


def user_resend_verification(*, email: Email):
    try:
        user = BaseUser.objects.get(email=email)
        if user.is_active:
            raise exceptions.UserAlreadyVerified
        verification_code = set_verification_code_to_redis(email=email)
        # TODO: Sending verification_code to user email
    except BaseUser.DoesNotExist:
        raise exceptions.NotActiveAccount