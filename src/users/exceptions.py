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


class PasswordIsWrong(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Password is wrong!"
    default_code = "password_is_wrong"


class InvalidVerificationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Verification code is invalid!(Expired or wrong)"
    default_code = "invalid_verification_code"


class UserAlreadyVerified(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User has already been verified!"
    default_code = "user_already_verified"


class NotActiveAccount(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Not active account found!"
    default_code = "not_active_account"
