from django.contrib import admin

from coins.models import Coin, Buy, Sell, CoinHolder
# Register your models here.


admin.site.register(Coin)
admin.site.register(Buy)
admin.site.register(CoinHolder)
admin.site.register(Sell)
