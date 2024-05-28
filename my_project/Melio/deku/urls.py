from django.urls import path
from .views import *

urlpatterns = [
    path("login/", user_login, name="login"),
    path("signup/", user_signup, name="signup"),
    path("forget_password/", forget_password, name="forget_password"),
    path("change_password/<str:token>", change_password, name="change_password"),
    path("logout/", user_logout, name="logout"),
    path("profile/", profile_update, name="profile"),
]
