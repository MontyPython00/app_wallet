from django.urls import path
from wallets import views

app_name = 'wallets'

urlpatterns = [
	path('', views.user_wallets_view, name='wallets'),
	path('wallet/<int:wallet_id>/', views.wallet_view, name='wallet'),
	path('create/', views.create_view, name='create'),
]