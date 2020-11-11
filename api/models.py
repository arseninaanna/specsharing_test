from django.db import models


CURRENCY_CHOICES = (
    ('EUR', 'Euro'),
    ('RUB', 'Rubble'),
    ('USD', 'Dollar'),
)


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

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
