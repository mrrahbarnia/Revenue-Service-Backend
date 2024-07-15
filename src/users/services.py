import logging

from django.core.exceptions import ValidationError

from .exceptions import UserAlreadyExists
from .models import BaseUser
from .types import Email, Password

logger = logging.getLogger("backend")


def user_register(*, email: Email, password: Password) -> BaseUser:
    try:
        user = BaseUser.objects.create_user(email=email, password=password)
        # TODO: Sending email to user
        return user
    except ValidationError:
        raise UserAlreadyExists
