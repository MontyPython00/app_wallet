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
	_market_cap = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=3, validators=[MinValueValidator(0)]), default=list, blank=True, null=True)
	_stocks_left = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=3, validators=[MinValueValidator(0)]), default=list, blank=True, null=True)
	# quantity - sum(stocks_left) =  stocks_left_to_buy

	def __str__(self):
		return f'{self.name}({self.symbol})'

	@property
	def market_cap(self):
		return sum(self._market_cap) * self.price
	
	@property
	def stocks_left(self):
		return self.quantity - sum(self._stocks_left)


	def get_absolute_url(self):
		return reverse('coins:coin', kwargs={'coin_id': self.id})

	def amount_of_holders(self):
		return self.holders.count()



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
	holder_wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)
	_avg_buy_price = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)]), default=list)
	_amount_of_coin = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)]), default=list)
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)

	@property
	def avg_buy_price(self):
		return sum(self._avg_buy_price) / len(self._avg_buy_price)

	@property
	def amount_of_coin(self):
		return sum(self._amount_of_coin)
	
	

#post signal 
#przy zakupie buy post_signal wysyla sygnal do aktualizacji modelow CoinHolder, Coin, Wallet
#Coin - market_cap(buy.amount_of_coin * coin.price), (quantity - sum(list(buy.amount_of_coin)), buy.wallet przypisany do holdera
#CoinHolder - wallet przypisany do walllet'a, avg_buy_price(sum(list(buy.total_price)) / amount_of_coin), amount_of_coin(sum(list(buy.amount_of_coin)))
#Coin holders jesli wlasciciel zejdzie z CoinHolder.amount_of_coin do 0 wowczas holder odejmuje o 1


@receiver(post_save, sender=Buy)
def buy_model_data_spreader(sender, instance, created, **kwargs):
	
	if created:
		obj_coin = Coin.objects.get(pk=instance.coin.id)
		obj_wallet = Wallet.objects.get(pk=instance.wallet.id)
		coin_holder_exists = CoinHolder.objects.filter(holder_wallet=obj_wallet).exists()
		#Wallet model
		obj_wallet.yang -= instance.total_price
		obj_wallet.save()
		# #Coin model
		obj_coin.holders.add(instance.wallet) # model Coin.holder update
		obj_coin._market_cap.append(instance.amount_of_coin) # model Coin.market_cap update
		obj_coin._stocks_left.append(instance.amount_of_coin) # model Coin.stocks_left update
		obj_coin.save()
		#CoinHolder model
		if coin_holder_exists:
			wallet_holder = CoinHolder.objects.get(holder_wallet=obj_wallet)
			wallet_holder._amount_of_coin.append(instance.amount_of_coin)
			wallet_holder._avg_buy_price.append(instance.total_price)
			wallet_holder.save()
		else:
			CoinHolder.objects.create(holder_wallet=obj_wallet, 
				coin=obj_coin, 
				_avg_buy_price=[instance.total_price], 
				_amount_of_coin=[instance.amount_of_coin])

 

#Dodaj sell button marketcap -, coinholder jesli ma 0 wowczas coin.holders -, jesli wallet ma 0 wowczas kasujemy, ale pytamy sie uzytkownika dane z coina
#przy sprzedazy sell post_signal aktualizauje, CoinHolder'a i Coin'a oraz Wallet'a
# W wallecie zostaje zaktualizowana ilosc yang
# W coinie jest aktulizowany market_cap, ilosc osob posiadajacych coiny jesli w coinholderze _amount_of_coin zostanie zrownana z zerem(mozna napisac to w modelu coinholder)
# _stocks_left
# W coinholderze aktualizujemy _amount_of_coin, _avg_buy_price, zastanow sie nad zachowaniem przy wyrownaniu z zerem(prawdopodobnie kasujemy cala instancje)


@receiver(post_save, sender=Sell)
def sell_model_data_spreader(sender, instance, created, **kwargs):
	if created:
		obj_wallet = instance.wallet
		obj_coin = instance.coin

		#Wallet model
		obj_wallet.yang += instance.total_price
		obj_wallet.save()
		#Coin model
		obj_coin._market_cap
		#zmieniamy model na decimalfield 
		#stocks left to samo na decimalfield


		#CoinHolder
		#dodaj settera ktory bedzie obliczal i zapamietywal liczbe aby mogl po jakims czasie zerowac ta ilosc 
		#amount_of_coin zmieniamy na decimalfield 




#PAMIETAJ ZEBY ZROBIC MIGRACJE I ZAKTUALIZOWAC MODELE 