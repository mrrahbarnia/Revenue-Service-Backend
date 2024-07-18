import logging

from typing import Any
from django.core.exceptions import ValidationError
from django.db.models import F

from common.dependencies import connect_redis
from .. import exceptions
from ..models import BaseUser
from ..types import Email, Password
from .dependencies import set_verification_code_to_redis, set_random_password_to_redis

logger = logging.getLogger("backend")


def user_register(*, email: Email, password: Password) -> BaseUser:
    try:
        user = BaseUser.objects.create_user(email=email, password=password)
        verification_code = set_verification_code_to_redis(email=email)
        # TODO: Sending verification_code to user's email
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
    user_email: Any = redis_connection.getdel(name=f"verification_code:{verification_code}")
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
        # TODO: Sending verification_code to user's email
    except BaseUser.DoesNotExist:
        raise exceptions.NotActiveAccount


def user_reset_password(*, email: Email) -> None:
    try:
        BaseUser.objects.get(email=email)
        random_password = set_random_password_to_redis(email=email)
        # TODO: Sending random_password to user's email
    except BaseUser.DoesNotExist:
        raise exceptions.NotActiveAccount


def user_verify_reset_password(received_password: str):
    redis_connection = connect_redis()
    user_email: Any = redis_connection.getdel(name=f"random_password:{received_password}")
    if user_email:
        user = BaseUser.objects.get(email=user_email.decode("ascii"))
        user.set_password(received_password)
        user.save(update_fields=["password"])
    else:
        raise exceptions.InvalidRandomPassword
