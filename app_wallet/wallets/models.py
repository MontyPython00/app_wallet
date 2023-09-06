from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class MainWallet(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)





class Wallet(models.Model):

	LEVELS_OF_EXPERIENCE = [
		('FRESH', 'Fresh'),
		('INTERMEDIATE', 'Intermediate'),
		('EXPERT', 'Expert')
	]

	main_wallet = models.ForeignKey(MainWallet, on_delete=models.CASCADE, null=False)
	name = models.CharField(max_length=16, null=False, blank=False)
	wallet_id = models.CharField(max_length=32, unique=True, null=False, blank=False)
	user_experience = models.CharField(max_length=12, choices=LEVELS_OF_EXPERIENCE, default='FRESH')
	yang = models.IntegerField(validators=[MinValueValidator(0)], default=0)
	active = models.BooleanField(default=False)
	

	def __str__(self):
		return f'{self.name}, {self.user_experience} '


	def get_absolute_url(self):
		return reverse('wallets:wallet', kwargs={'wallet_id': self.id})


	def clean(self):
		#If wallet is updated
		if self.id is not None:
			is_any_other_wallet_active = Wallet.objects.filter(main_wallet=self.main_wallet, active=True).exclude(id=self.id)
			if is_any_other_wallet_active:
				raise ValidationError(f'{is_any_other_wallet_active.first().name} is active')

			is_wallet_name_unique = Wallet.objects.filter(main_wallet=self.main_wallet, name__iexact=self.name).exclude(id=self.id)
			if is_wallet_name_unique:
				raise ValidationError(f'{self.name} is already taken.')

	






@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
	if created:
		MainWallet.objects.create(user=instance)
