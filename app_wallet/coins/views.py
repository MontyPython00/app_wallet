from django.shortcuts import render

from coins.models import Coin
# Create your views here.



def coins_view(request):
	coins = Coin.objects.all()
	context = {
		'coins': coins,
	}

	return render(request, 'coins/home_page.html', context=context)