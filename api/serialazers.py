from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class WalletSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    balance = serializers.FloatField()
    currency = serializers.CharField()


class CurrencyMapSerializer(serializers.Serializer):
    currency_code = serializers.CharField()
    value = serializers.IntegerField()
