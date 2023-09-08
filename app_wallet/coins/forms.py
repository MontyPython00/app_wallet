from django import forms
from django.core.exceptions import ValidationError

from coins.models import Buy, Coin, Sell



class BuyForm(forms.ModelForm):
	class Meta:
		model = Buy
		fields = ['amount_of_coin', 'total_price']

	def __init__(self, *args, **kwargs):
		self.coin_identifier = kwargs.pop('coin_identifier')
		self.wallet = kwargs.pop('wallet')
		super(BuyForm, self).__init__(*args, **kwargs)

	def clean_amount_of_coin(self):
		amount_of_coin = self.cleaned_data.get('amount_of_coin')
		left_quantity_of_coin = Coin.objects.get(id=self.coin_identifier).stocks_left
		if left_quantity_of_coin < amount_of_coin:
			raise ValidationError(f'You cannot buy that many coins, Coins left:{left_quantity_of_coin}')

		return amount_of_coin

	def clean_total_price(self):
		total_price = self.cleaned_data.get('total_price')
		if total_price > self.wallet.yang:
			raise ValidationError(f'Wallet has not enough yang to complete buy, Add:{total_price - self.wallet.yang} ')

		return total_price



class SellForm(forms.ModelForm):
	class Meta:
		model = Sell
		fields = ['amount_of_coin', 'total_price']