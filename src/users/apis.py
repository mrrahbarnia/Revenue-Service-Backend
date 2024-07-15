from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import PasswordsNotMatch
from .services import user_register
from .validators import letter_validator, number_validator, special_char_validator


class UserRegisterApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(
            validators=(
                MinLengthValidator(limit_value=8),
                number_validator,
                letter_validator,
                special_char_validator,  # type: ignore
            )
        )
        confirm_password = serializers.CharField()

        def validate(self, attrs: dict) -> dict:
            password = attrs.get("password")
            confirm_password = attrs.get("confirm_password")
            if password != confirm_password:
                raise PasswordsNotMatch
            return attrs

    @extend_schema(request=InputSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_register(
            email=serializer.validated_data.get("email"),
            password=serializer.validated_data.get("password"),
        )
        return Response(
            {"message": "Registered successfully"}, status=status.HTTP_201_CREATED
        )
