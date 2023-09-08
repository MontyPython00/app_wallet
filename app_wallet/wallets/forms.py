from django import forms
from django.contrib.auth import get_user_model
from wallets.models import Wallet
from django.core.exceptions import ValidationError

class CreateWalletForm(forms.ModelForm):
	name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
	wallet_id = forms.CharField(label='Wallet ID', widget=forms.TextInput(attrs={'placeholder': 'Id'}))

	class Meta:
		model = Wallet
		fields = ['name', 'wallet_id', 'user_experience']

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(CreateWalletForm, self).__init__(*args, **kwargs)
		
	#If wallet is created  form clean does work 
	def clean(self):
		wallet_names = Wallet.objects.filter(main_wallet__user=self.user, name__iexact=self.cleaned_data['name']).exists()
		if wallet_names:
			raise ValidationError('name is already taken')

		return self.cleaned_data






#If wallet is updated model validation works
class UpdateWalletForm(forms.ModelForm):
	name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
	wallet_id = forms.CharField(label='Wallet ID', widget=forms.TextInput(attrs={'placeholder': 'Id'}))

	class Meta:
		model = Wallet
		fields = ['name', 'wallet_id', 'user_experience', 'active']

	
