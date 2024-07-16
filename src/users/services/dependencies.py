from uuid import uuid4
from django.conf import settings

from common.dependencies import connect_redis
from ..types import Email


def set_verification_code_to_redis(*, email: Email) -> str:
    verification_code = (uuid4().hex)[0:7] # Example => 'd33b1ff'
    redis_connection = connect_redis()
    redis_connection.set(
        name=f"verification_code:{verification_code}", value=email,
        ex=int(settings.VERIFICATION_EMAIL_EXPIRY_SEC)
    ) # Example => key: 'd33b1ff', value: user@example.com
    return verification_code


def set_random_password_to_redis(*, email: Email) -> str:
    random_password = (uuid4().hex)[0:10] # Example => '3b1ffjnad9'
    redis_connection = connect_redis()
    redis_connection.set(
        name=f"random_password:{random_password}", value=email,
        ex=int(settings.VERIFICATION_EMAIL_EXPIRY_SEC)
    ) # Example => key: 'd33b1ff', value: user@example.com
    return random_password
