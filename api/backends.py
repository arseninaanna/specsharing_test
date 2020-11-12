from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import (
    check_password, make_password,
)
from .models import User


class UserHelper:
    _user = None

    def __init__(self, user):
        self._user = user

    def check_password(self, password):
        return check_password(password, self._user.password)

    @staticmethod
    def get_password_hash(password):
        return make_password(password)


class AuthBackend(ModelBackend):
    def get_user(self, user_id):
        return User.objects.get(pk=user_id)

    def authenticate(self, request, email=None, username=None, password=None, **kwargs):
        if email is None:
            email = username

        if not email and not password:
            raise Exception("Missed required arguments")

        try:
            user = User.objects.get(email=email)
            helper = UserHelper(user)
        except User.DoesNotExist:
            raise Exception("Such user does not exist")

        if helper.check_password(password):
            return user

    def get_user_permissions(self, user_obj, obj=None):
        return set()

    def get_group_permissions(self, user_obj, obj=None):
        return set()

    def get_all_permissions(self, user_obj, obj=None):
        return set()

    def has_perm(self, user_obj, perm, obj=None):
        return True

    def has_module_perms(self, user_obj, app_label):
        return True
