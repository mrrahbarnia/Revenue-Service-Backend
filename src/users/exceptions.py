from rest_framework import status
from rest_framework.exceptions import APIException


class PasswordsNotMatch(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Passwords must be match!"
    default_code = "passwords_must_match"


class UserAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "User already exists!"
    default_code = "user_already_exists"
