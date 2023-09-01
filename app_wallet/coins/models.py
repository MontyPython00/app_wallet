from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator

# Create your models here.


class Coin(models.Model):
	name = models.CharField(max_length=32, null=False, blank=False, unique=True, validators=[MinLengthValidator(4)])
	symbol = models.CharField(max_length=8, null=False, blank=False, unique=True, validators=[MinLengthValidator(2)])
	price = models.IntegerField(validators=[MinValueValidator(0)], null=False, blank=False)


	def __str__(self):
		return f'{self.name}({self.symbol}), {self.price}'
