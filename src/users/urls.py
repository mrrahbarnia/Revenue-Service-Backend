from django.urls import path

from . import apis

app_name = "users"


urlpatterns = [
    path("register/", apis.UserRegisterApi.as_view(), name="register"),
]
