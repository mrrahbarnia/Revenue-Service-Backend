import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .types import Password


def number_validator(password: Password):
    regex = re.compile("[0-9]")
    if regex.search(password) is None:
        raise ValidationError(
            _("Password must contain numbers."), code="password_contain_numbers"
        )


def letter_validator(password: Password):
    regex = re.compile("[a-zA-Z]")
    if regex.search(password) is None:
        raise ValidationError(
            _("Password must contain letters."), code="password_contain_letters"
        )


def special_char_validator(password: Password):
    regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    if regex.search(password) is None:
        raise ValidationError(
            _("Password must contain special character."),
            code="password_contain_special_char",
        )
