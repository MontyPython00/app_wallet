from django.urls import path

from coins import views


app_name = 'coins'

urlpatterns=[
	path('', views.coins_view, name='coins'),
	path('create/', views.create_view, name='create'),
	path('<int:coin_id>/', views.coin_detail, name='coin')
]