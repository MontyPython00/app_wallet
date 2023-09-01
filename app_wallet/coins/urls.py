from django.urls import path

from coins import views


app_name = 'coins'

urlpatterns=[
	path('', views.coins_view, name='coins'),
]