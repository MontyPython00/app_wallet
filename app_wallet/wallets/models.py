from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.core.exceptions import ValidationError
from coins.models import Coin

# Create your models here.



class Wallet(models.Model):

	LEVELS_OF_EXPERIENCE = [
		('FRESH', 'Fresh'),
		('INTERMEDIATE', 'Intermediate'),
		('EXPERT', 'Expert')
	]

	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	name = models.CharField(max_length=16, null=False, blank=False)
	wallet_id = models.CharField(max_length=32, unique=True)
	user_experience = models.CharField(max_length=12, choices=LEVELS_OF_EXPERIENCE, default='FRESH')
	yang = models.IntegerField(validators=[MinValueValidator(0)], default=0)
	holders = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return f'{self.name}, {self.user_experience}'


	def get_absolute_url(self):
		return reverse('wallets:wallet', kwargs={'wallet_id': self.id})



