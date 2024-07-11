from redis import Redis
from django.conf import settings


def connect_redis() -> Redis:
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)