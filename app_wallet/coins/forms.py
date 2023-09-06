from django import forms

from coins.models import Coin


class CoinAddHolder(forms.ModelForm):

	class Meta:
		model = Coin
		fields = ['quantity']