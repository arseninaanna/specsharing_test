from django.db import models
from .managers import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


CURRENCY_CHOICES = (
    ('EUR', 'Euro'),
    ('RUB', 'Rubble'),
    ('USD', 'Dollar'),
)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    groups = None
    user_permissions = None

    is_staff = True

    @property
    def is_superuser(self):
        return self.email == 'a@mail.ru'  # hack for easy development

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    def __str__(self):
        return '{} {} {}'.format(self.user, self.currency, self.balance)


class CurrencyMap(models.Model):
    currency_code = models.CharField(max_length=3)
    value = models.FloatField()

    def __str__(self):
        return self.currency_code
