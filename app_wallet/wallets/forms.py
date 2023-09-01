from django import forms
from django.contrib.auth import get_user_model
from wallets.models import Wallet
from django.core.exceptions import ValidationError

class CreateWalletForm(forms.ModelForm):
	name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
	wallet_id = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Id'}))

	class Meta:
		model = Wallet
		fields = ['name', 'wallet_id', 'user_experience']

	
	def clean_name(self):
		name = self.cleaned_data['name']
		wallets_name = Wallet.objects.filter(name=name)
		print(name, wallets_name)
		if len(wallets_name) > 0:
			raise ValidationError(f'{name} is already used.')
		return name


	
