from django import forms
from django.contrib.auth import get_user_model
from wallets.models import Wallet


class CreateWalletForm(forms.ModelForm):
	wallet_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
	wallet_id = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Id'}))

	class Meta:
		model = Wallet
		fields = ['wallet_name', 'wallet_id', 'user_experience']

	
		


