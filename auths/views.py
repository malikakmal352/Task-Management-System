from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View

from auths import helper
from auths.helper import RequiredLoginRequiredMixin
from auths.models import User


class Login(RequiredLoginRequiredMixin, View):
    @staticmethod
    def get(request):
        return render(request, "login.html")

    @staticmethod
    def post(request):
        Data = request.POST
        email = Data.get("email")
        user_password = Data.get("password")
        print("email ============>", email, user_password)
        message, user = helper.login_validate(email, user_password)
        if message:
            messages.error(request, message)
            return redirect("/auth/")
        else:
            login(request, user)
        return redirect("/")


class SignUp(RequiredLoginRequiredMixin, View):
    @staticmethod
    def get(request):
        return render(request, "signup.html")

    @staticmethod
    def post(request):
        Data = request.POST
        password = Data.get("password")
        email = Data.get("email", None)
        username = Data.get("username")

        message = helper.validate_data(email)
        if message:
            messages.error(request, message)
        else:
            User.create_user(email, password, username)
            messages.success(
                request, "Account Created"
            )
            return redirect("/auth/")
        return redirect("/auth/signup/")
