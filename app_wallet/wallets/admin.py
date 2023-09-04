from django.contrib import admin
from wallets.models import Wallet, MainWallet

# Register your models here.

admin.site.register(MainWallet)

admin.site.register(Wallet)