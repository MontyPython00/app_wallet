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
	market_cap = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=5, validators=[MinValueValidator(0)]), default=list, blank=True, null=True)
	stocks_left = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=5, validators=[MinValueValidator(0)]), default=list, blank=True, null=True)
	# quantity - sum(stocks_left) =  stocks_left_to_buy
	def __str__(self):
		return f'{self.name}({self.symbol}), {self.price}'


	def get_absolute_url(self):
		return reverse('coins:coin', kwargs={'coin_id': self.id})

	def amount_of_holders(self):
		return self.holders.count()

	def get_market_cap(self):
		return sum(self.market_cap) * self.price


	

class Buy(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False)
	amount_of_coin = models.DecimalField(max_digits=16, decimal_places=5, validators=[MinValueValidator(0)])
	total_price = models.DecimalField(max_digits=16, decimal_places=5, validators=[MinValueValidator(0)])
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)



class CoinHolder(models.Model):
	holder_wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)
	avg_buy_price = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=5, validators=[MinValueValidator(0)]), default=list)
	amount_of_coin = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=5, validators=[MinValueValidator(0)]), default=list)
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)


#post signal 
#przy zakupie buy post_signal wysyla sygnal do aktualizacji modelow CoinHolder, Coin
#Coin - market_cap(buy.amount_of_coin * coin.price), (quantity - sum(list(buy.amount_of_coin)), buy.wallet przypisany do holdera
#CoinHolder - wallet przypisany do walllet'a, avg_buy_price(sum(list(buy.total_price)) / amount_of_coin), amount_of_coin(sum(list(buy.amount_of_coin)))
#Coin holders jesli wlasciciel zejdzie z CoinHolder.amount_of_coin do 0 wowczas holder odejmuje o 1


@receiver(post_save, sender=Buy)
def buy_model_data_spreader(sender, instance, created, **kwargs):
	
	if created:
		obj_coin = Coin.objects.get(pk=instance.coin.id)
		obj_wallet = Wallet.objects.get(pk=instance.wallet.id)
		coin_holder_exists = CoinHolder.objects.filter(holder_wallet=obj_wallet).exists()

		# #Coin model
		obj_coin.holders.add(instance.wallet) # model Coin.holder update
		obj_coin.market_cap.append(instance.amount_of_coin) # model Coin.market_cap update
		obj_coin.stocks_left.append(instance.amount_of_coin) # model Coin.stocks_left update
		obj_coin.save()
		#CoinHolder model
		if coin_holder_exists:
			wallet_holder = CoinHolder.objects.get(holder_wallet=obj_wallet)
			wallet_holder.amount_of_coin.append(instance.amount_of_coin)
			wallet_holder.avg_buy_price.append(instance.total_price)
			wallet_holder.save()
		else:
			CoinHolder.objects.create(holder_wallet=obj_wallet, 
				coin=obj_coin, 
				avg_buy_price=[instance.total_price], 
				amount_of_coin=[instance.amount_of_coin])

 

