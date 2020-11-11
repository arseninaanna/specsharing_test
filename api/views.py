from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Wallet, CurrencyMap
from .serialazers import UserSerializer, WalletSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.http import Http404


class UserView(APIView):
    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})


class WalletView(APIView):
    def get(self, request):
        wallets = Wallet.objects.all()

        serializer = WalletSerializer(wallets, many=True)
        return Response({"wallets": serializer.data})


@api_view(['GET'])
def withdraw(request, pk):
    curr_wallet = get_object_or_404(Wallet.objects.all(), pk=pk)
    amount = float(request.GET.get('amount'))

    if float(amount) > curr_wallet.balance:
        raise Http404("Not enough balance")
    else:
        curr_wallet.balance -= amount
        curr_wallet.save()
        return Response({"wallet's balance reduced by": amount})


@api_view(['GET'])
def replenish(request, pk):
    curr_wallet = get_object_or_404(Wallet.objects.all(), pk=pk)
    amount = float(request.GET.get('amount'))

    curr_wallet.balance += amount
    curr_wallet.save()
    return Response({"wallet's balance replenished by": amount})


@api_view(['GET'])
def transfer(request, pk):
    sender_wallet = get_object_or_404(Wallet.objects.all(), pk=pk)
    sender_currency = sender_wallet.currency
    amount = float(request.GET.get('amount'))
    recipient_pk = int(request.GET.get('recipient'))

    if float(amount) > sender_wallet.balance:
        raise Http404("Not enough balance")

    try:
        recipient_wallet = get_object_or_404(Wallet.objects.all(), pk=recipient_pk)
        recipient_currency = recipient_wallet.currency
    except Exception:
        raise Http404("No such recipient")

    if recipient_wallet.user_id == sender_wallet.user_id:
        raise Http404("You can't transfer to the same wallet")

    if recipient_currency != sender_currency:
        if sender_currency == "RUB":
            recipient_rate = CurrencyMap.objects.get(currency_code=recipient_currency)
            recipient_wallet.balance += amount / recipient_rate.value
        elif recipient_currency == "RUB":
            sender_rate = CurrencyMap.objects.get(currency_code=sender_currency)
            recipient_wallet.balance += amount * sender_rate.value
        else:
            recipient_rate = CurrencyMap.objects.get(currency_code=recipient_currency)
            sender_rate = CurrencyMap.objects.get(currency_code=sender_currency)
            recipient_wallet.balance += (sender_rate.value * amount) / recipient_rate.value
    else:
        recipient_wallet.balance += amount

    sender_wallet.balance -= amount
    sender_wallet.save()
    recipient_wallet.save()

    return Response({"transfer was initiated": amount})


# @api_view(['GET'])
# def convert(request):
#     pass
