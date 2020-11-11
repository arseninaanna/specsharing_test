from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Wallet
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


# @api_view(['GET', 'PUT', 'DELETE'])
# def transfer(request):
#     pass
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def convert(request):
#     pass
