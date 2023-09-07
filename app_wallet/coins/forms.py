from django import forms

from coins.models import Buy



class BuyForm(forms.ModelForm):
	class Meta:
		model = Buy
		fields = ['amount_of_coin', 'total_price']