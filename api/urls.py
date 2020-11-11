from django.urls import path
from .views import UserView, WalletView
from api import views


app_name = "api"

urlpatterns = [
    path('users/', UserView.as_view()),
    path('wallets/', WalletView.as_view()),
    path('wallet/<int:pk>/withdraw', views.withdraw),
    path('wallet/<int:pk>/replenish', views.replenish),
    path('wallet/<int:pk>/transfer', views.transfer),
]
