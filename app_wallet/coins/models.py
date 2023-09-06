from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MinLengthValidator
from wallets.models import Wallet
from django.urls import reverse
# Create your models here.


class Coin(models.Model):
	name = models.CharField(max_length=32, null=False, blank=False, unique=True, validators=[MinLengthValidator(4)])
	symbol = models.CharField(max_length=8, null=False, blank=False, unique=True, validators=[MinLengthValidator(2)])
	price = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)
	holders = models.ManyToManyField(Wallet, blank=True)
	quantity = models.DecimalField(max_digits=16, decimal_places=5,validators=[MinValueValidator(0)])
	market_cap = ArrayField(base_field=models.DecimalField(max_digits=16, decimal_places=5, validators=[MinValueValidator(0)]),
	 default=list) 

	def __str__(self):
		return f'{self.name}({self.symbol}), {self.price}'


	def get_absolute_url(self):
		return reverse('coins:coin', kwargs={'coin_id': self.id})

	def amount_of_holders(self):
		return self.holders.count()
	

