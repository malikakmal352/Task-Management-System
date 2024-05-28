from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from auths.models import User


def validate_data(email):
    message = None
    try:
        if User.objects.get(email=email):
            message = "Email is already exist"
        return message
    except Exception:
        return message


def login_validate(email, user_password):
    try:
        message = None
        user = User.objects.get(email=email)
        if not user.is_active:
            message = "You Account is deactivated"
        elif not check_password(user_password, user.password):
            message = "Invalid E-mail or Password"
        return message, user
    except Exception:
        message = "Invalid E-mail or Password"
        return message, None


def change_password_validate(self, user_id, current_password, new_password):
    try:
        message = None
        user = User.objects.get(id=user_id)
        if not user.is_active:
            message = "You Account is deactivated"
        elif not check_password(current_password, user.password):
            message = "Invalid current Password"
        else:
            user.set_password(new_password)
            user.save()
            # Update the session with the new password hash
            update_session_auth_hash(self.request, user)
        return message
    except Exception:
        message = "Invalid user id or user not found"
        return message


class UserLoginRequiredMixin(LoginRequiredMixin):
    login_url = "/auth/"

    def handle_no_permission(self):
        return self.redirect_to_login(self.request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            login_url = self.login_url
            next_page_url = self.request.get_full_path()
            full_path = str(login_url + "?next=" + next_page_url)
            return redirect(full_path)


class RequiredLoginRequiredMixin:
    def handle_no_permission(self):
        return self.redirect_to_login(self.request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)
