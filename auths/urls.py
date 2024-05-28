from django.contrib.auth.views import LogoutView
from django.urls import path

from auths import views

urlpatterns = [
    path("", views.Login.as_view(), name="user_Login"),
    path("signup/", views.SignUp.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="/login/"), name="Logout"),
]
