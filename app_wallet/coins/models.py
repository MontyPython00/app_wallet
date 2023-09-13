from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MinLengthValidator
from wallets.models import Wallet
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Coin(models.Model):
	name = models.CharField(max_length=32, null=False, blank=False, unique=True, validators=[MinLengthValidator(4)])
	symbol = models.CharField(max_length=8, null=False, blank=False, unique=True, validators=[MinLengthValidator(2)])
	price = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
	holders = models.ManyToManyField(Wallet, blank=True)
	quantity = models.DecimalField(max_digits=16, decimal_places=5,validators=[MinValueValidator(0)])
	market_cap = models.DecimalField(max_digits=16, decimal_places=3, validators=[MinValueValidator(0)], default=0)
	_stocks_left = models.DecimalField(max_digits=16, decimal_places=3, validators=[MinValueValidator(0)], default=0)
	

	def __str__(self):
		return f'{self.name}({self.symbol})'


	def get_absolute_url(self):
		return reverse('coins:coin', kwargs={'coin_id': self.id})

	def amount_of_holders(self):
		return self.holders.count()

	@property
	def stocks_left(self):
		return self.quantity + self._stocks_left 
	



class Buy(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False)
	amount_of_coin = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
	total_price = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)


class Sell(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	amount_of_coin = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
	total_price = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)

class CoinHolder(models.Model):
	holder_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)
	_avg_buy_price = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)]), default=list)
	amount_of_coin = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)], null=True)
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)

	@property
	def avg_buy_price(self):
		sum_of_price_buy = self._avg_buy_price[0]
		amount_of_coin_on_wallet = self._avg_buy_price[1]
		return  sum_of_price_buy / amount_of_coin_on_wallet if sum_of_price_buy > 0 and amount_of_coin_on_wallet > 0 else 0

	
	

#post signal 
#przy zakupie buy post_signal wysyla sygnal do aktualizacji modelow CoinHolder, Coin, Wallet
#Coin - market_cap(buy.amount_of_coin * coin.price), (quantity - sum(list(buy.amount_of_coin)), buy.wallet przypisany do holdera
#CoinHolder - wallet przypisany do walllet'a, avg_buy_price(sum(list(buy.total_price)) / amount_of_coin), amount_of_coin(sum(list(buy.amount_of_coin)))
#Coin holders jesli wlasciciel zejdzie z CoinHolder.amount_of_coin do 0 wowczas holder odejmuje o 1


# @receiver(post_save, sender=Buy)
# def buy_model_data_spreader(sender, instance, created, **kwargs):
	
# 	if created:
# 		obj_coin = Coin.objects.get(pk=instance.coin.id)
# 		# obj_wallet = Wallet.objects.filter(pk=instance.wallet.id, coin=obj_coin).first()
# 		coin_holder_exists = CoinHolder.objects.filter(holder_wallet=instance.wallet, coin=instance.coin).exists()
		
# 		# #Coin model
# 		obj_coin.holders.add(instance.wallet) # model Coin.holder update // zastanow sie czy to z sellem ma w ogole racje bytu 
# 		obj_coin.market_cap += instance.total_price # model Coin.market_cap update
# 		obj_coin._stocks_left -= instance.amount_of_coin # model Coin.stocks_left update
# 		obj_coin.save()
# 		#CoinHolder model
# 		if coin_holder_exists:
# 			wallet_holder = CoinHolder.objects.get(holder_wallet=instance.wallet, coin=instance.coin)
# 			wallet_holder.amount_of_coin += instance.amount_of_coin
# 			wallet_holder._avg_buy_price[0] += instance.total_price#.append(instance.total_price)
# 			wallet_holder._avg_buy_price[1] += instance.amount_of_coin
# 			wallet_holder.save()
# 		else:
# 			new_wallet = CoinHolder.objects.create(holder_wallet=obj_wallet, 
# 				coin=obj_coin, 
# 				_avg_buy_price=[instance.total_price, instance.amount_of_coin],  
# 				amount_of_coin=instance.amount_of_coin)
# 			new_wallet.save()

#  		#Wallet model
# 		# obj_wallet = Wallet.objects.filter(pk=instance.wallet.id, coin=obj_coin).first()
# 		# coin_holder_exists = CoinHolder.objects.filter(holder_wallet=obj_wallet).exists()
# 		instance.wallet.yang -= instance.total_price
# 		instance.wallet.save()


@receiver(post_save, sender=Buy)
def buy_model_data_spreader(sender, instance, created, **kwargs):
	if created:
		coin = instance.coin
		wallet = instance.wallet

		#Coin model
		coin.holders.add(instance.wallet)
		coin.market_cap += instance.total_price
		coin._stocks_left -= instance.amount_of_coin
		coin.save()

		#CoinHolder
		wallet_holder = CoinHolder.objects.filter(holder_wallet=wallet, coin=coin)
		if wallet_holder.exists():
			wallet_holder_true = wallet_holder.first()
			wallet_holder_true.amount_of_coin += instance.amount_of_coin
			wallet_holder_true._avg_buy_price[0] += instance.total_price
			wallet_holder_true._avg_buy_price[1] += instance.amount_of_coin
			wallet_holder_true.save()
		else:
			new_wallet_holder = CoinHolder.objects.create(holder_wallet=wallet, 
				coin=coin,
				_avg_buy_price=[instance.total_price, instance.amount_of_coin],
				amount_of_coin=instance.amount_of_coin)
			new_wallet_holder.save()

		#Wallet
		wallet.yang -= instance.total_price
		wallet.save()


#Dodaj sell button marketcap -, coinholder jesli ma 0 wowczas coin.holders -, jesli wallet ma 0 wowczas kasujemy, ale pytamy sie uzytkownika dane z coina
#przy sprzedazy sell post_signal aktualizauje, CoinHolder'a i Coin'a oraz Wallet'a
# W wallecie zostaje zaktualizowana ilosc yang
# W coinie jest aktulizowany market_cap, ilosc osob posiadajacych coiny jesli w coinholderze _amount_of_coin zostanie zrownana z zerem(mozna napisac to w modelu coinholder)
# _stocks_left
# W coinholderze aktualizujemy _amount_of_coin, _avg_buy_price, zastanow sie nad zachowaniem przy wyrownaniu z zerem(prawdopodobnie kasujemy cala instancje)


# @receiver(post_save, sender=Sell)
# def sell_model_data_spreader(sender, instance, created, **kwargs):
# 	if created:
# 		obj_wallet = instance.wallet
# 		obj_coin = instance.coin
# 		obj_holder_wallet = CoinHolder.objects.filter(holder_wallet=instance.wallet, coin=obj_coin).first()

# 		#Wallet model
# 		obj_wallet.yang += instance.total_price
# 		obj_wallet.save()
# 		#Coin model
# 		obj_coin.market_cap -= instance.total_price
# 		obj_coin._stocks_left += instance.amount_of_coin
# 		obj_coin.save()

# 		#CoinHolder
# 		obj_holder_wallet.amount_of_coin -= instance.amount_of_coin 
# 		# obj_holder_wallet.save()
# 		if obj_holder_wallet.amount_of_coin > 0:
# 			avg_buy_of_previous_group = obj_holder_wallet._avg_buy_price[0] / obj_holder_wallet._avg_buy_price[1]
# 			obj_holder_wallet._avg_buy_price[0] = avg_buy_of_previous_group
# 			obj_holder_wallet._avg_buy_price[1] = 1 #srednia arytmetyczna zakupu jest liczona jako jeden zakup od momentu pierwszej sprzedazy

# 		else:
# 			obj_coin.holders.remove(instance.wallet)
# 			obj_holder_wallet._avg_buy_price[0] = 0
# 			obj_holder_wallet._avg_buy_price[1] = 0 # przy wyzerowaniu walleta zerujemy tez sredni zakup
# 		obj_holder_wallet.save()


@receiver(post_save, sender=Sell)
def sell_model_data_spreader(sender, instance, created, **kwargs):
	if created:
		coin = instance.coin
		wallet = instance.wallet
		coin_holder = CoinHolder.objects.get(holder_wallet=wallet, coin=coin)

		#CoinHolder model
		coin_holder.amount_of_coin -= instance.amount_of_coin
		if coin_holder.amount_of_coin == 0:
			coin.holders.remove(wallet) #Coin model
			coin_holder._avg_buy_price[0] = 0
			coin_holder._avg_buy_price[1] = 0
		else:
			previous_avg_buy = coin_holder._avg_buy_price[0] / coin_holder._avg_buy_price[1] #0 - sum_buy_price | 1 - amount_of_coins 
			coin_holder._avg_buy_price[0] = previous_avg_buy
			coin_holder._avg_buy_price[1] = 1 #srednia arytmetyczna poprzednich zakupow zamienia sie w jeden zakup i liczona jest jako grupa zakupow
			#aby moc obliczyc srednia przy kolejnych zakupach po sprzedazy
		coin_holder.save() 

		#Wallet model
		wallet.yang += instance.total_price

		#Coin model
		coin.market_cap -= instance.total_price
		coin._stocks_left += instance.amount_of_coin
		coin.save()

