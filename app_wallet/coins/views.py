from django.shortcuts import render, redirect, get_object_or_404

from coins.forms import CoinAddHolder
from coins.models import Coin
from wallets.models import Wallet
# Create your views here.



def coins_view(request):
	coins = Coin.objects.all()
	context = {
		'coins': coins,
	}

	return render(request, 'coins/home_page.html', context=context)


def coin_detail(request, coin_id):
	coin = get_object_or_404(Coin, id=coin_id)
	form = CoinAddHolder(request.POST or None, instance=coin)
	holder = Wallet.objects.get(main_wallet__user=request.user, active=True)
	
	if form.is_valid():
		obj = form.save(commit=False)
		obj.holders.set([holder])
		obj.save()
		

	context = {
		'coin': coin,
		'form': form,
	}

	return render(request, 'coins/coin.html', context=context)