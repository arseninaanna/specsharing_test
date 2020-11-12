from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Wallet, CurrencyMap
from .serialazers import UserSerializer, WalletSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny


class UserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})


class WalletView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        wallets = Wallet.objects.all()

        serializer = WalletSerializer(wallets, many=True)
        return Response({"wallets": serializer.data})


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, email=email, password=password)
    if not user:
        message = "There is no such user"
        status = 404
        return JsonResponse({'message': message}, status=status)

    token, _ = Token.objects.get_or_create(user_id=user.id)
    return Response({'token': token.key})


@api_view(['GET'])
@permission_classes([AllowAny])
def withdraw(request, pk):
    """
    GET params: amount - amount to withdraw in the currency of operated wallet
    :param pk: primary key of wallet to be operated
    """

    curr_wallet = get_object_or_404(Wallet.objects.all(), pk=pk)
    amount = float(request.GET.get('amount'))

    if float(amount) > curr_wallet.balance:
        message = "Not enough balance"
        status = 400
    else:
        curr_wallet.balance -= amount
        curr_wallet.save()
        status = 200
        message = "wallet's balance reduced by {}".format(amount)

    return JsonResponse({'message': message}, status=status)


@api_view(['GET'])
@permission_classes([AllowAny])
def replenish(request, pk):
    """
    GET params: amount - amount to replenish in the currency of operated wallet
    :param pk: primary key of wallet to be operated
    """

    curr_wallet = get_object_or_404(Wallet.objects.all(), pk=pk)
    amount = float(request.GET.get('amount'))

    curr_wallet.balance += amount
    curr_wallet.save()
    return Response({"wallet's balance replenished by": amount})


@api_view(['GET'])
@permission_classes([AllowAny])
def transfer(request, pk):
    """
    Transfer between own wallets
    Transfer from own wallet to other user's wallet

    If currency of recipient's wallet differs from sender,
    before replenish recipient's wallet convertation is performed

    GET params:
    - amount: amount to replenish in the currency of operated wallet
    - recipient: primary key of recipient's wallet
    :param pk: primary key of wallet to be withdrawed
    """

    sender_wallet = get_object_or_404(Wallet.objects.all(), pk=pk)
    sender_currency = sender_wallet.currency
    amount = float(request.GET.get('amount'))
    recipient_pk = int(request.GET.get('recipient'))

    if float(amount) > sender_wallet.balance:
        message = "Not enough balance"
        status = 400
        return JsonResponse({'message': message}, status=status)

    try:
        recipient_wallet = get_object_or_404(Wallet.objects.all(), pk=recipient_pk)
        recipient_currency = recipient_wallet.currency
    except Exception:
        message = "No such recipient"
        status = 400
        return JsonResponse({'message': message}, status=status)

    if recipient_wallet.id == sender_wallet.id:
        message = "You can't transfer to the same wallet"
        status = 400
        return JsonResponse({'message': message}, status=status)

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
    recipient_wallet.balance = round(recipient_wallet.balance, 2)
    sender_wallet.save()
    recipient_wallet.save()

    return Response({"transfer was initiated": amount})

