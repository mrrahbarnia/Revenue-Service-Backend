from typing import Dict, Any
from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView

from .exceptions import PasswordsNotMatch, InvalidVerificationCode
from . import services
from .validators import letter_validator, number_validator, special_char_validator


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token["is_admin"] = user.is_staff
        return token
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data["email"] = self.user.email # type: ignore
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer # type: ignore


class UserRegisterApi(APIView):
    class RegisterInSerializer(serializers.Serializer):
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

    @extend_schema(request=RegisterInSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.RegisterInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.user_register(
            email=serializer.validated_data.get("email"),
            password=serializer.validated_data.get("password"),
        )
        return Response(
            {"message": "Registered successfully"}, status=status.HTTP_201_CREATED
        )


class UserVerifyAccountApi(APIView):
    class VerifyAccountSerializer(serializers.Serializer):
        verification_code = serializers.CharField()

        def validate_verification_code(self, value: str) -> str:
            if len(value) != 7:
                raise InvalidVerificationCode
            return value

    @extend_schema(request=VerifyAccountSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.VerifyAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.user_verify_account(
            verification_code=serializer.validated_data.get("verification_code")
        )
        return Response(
            {"message": "Account verified successfully"}, status=status.HTTP_200_OK
        )


class UserResendVerificationApi(APIView):
    class ResendVerificationSerializer(serializers.Serializer):
        email = serializers.CharField()
    
    @extend_schema(request=ResendVerificationSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.user_resend_verification(
            email=serializer.validated_data.get("email")
        )
        return Response(
            {"message": "Verification code resent."}, status=status.HTTP_200_OK
        )


class UserChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]
    class ChangePassInSerializer(serializers.Serializer):
        old_password = serializers.CharField()
        new_password = serializers.CharField()
        confirm_password = serializers.CharField()

        def validate(self, attrs: dict) -> dict:
            new_password = attrs.get("new_password")
            confirm_password = attrs.get("confirm_password")
            if new_password != confirm_password:
                raise PasswordsNotMatch
            return attrs
        
    @extend_schema(request=ChangePassInSerializer)
    def post(self, request: Request) -> Response:
        serializer = self.ChangePassInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.user_change_password(
            user=request.user, # type: ignore
            old_password=serializer.validated_data.get("old_password"),
            new_password=serializer.validated_data.get("new_password")
        )
        return Response(
            {"message": 'Password changed successfully'}, status=status.HTTP_200_OK
        )
            