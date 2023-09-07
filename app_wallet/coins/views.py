from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from coins.forms import BuyForm
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
	form = BuyForm(request.POST or None)
	holder = Wallet.objects.get(main_wallet__user=request.user, active=True)	#AS DEFAULT NONE WALLET IS ACTIVE DEAL WITH IT 
	if form.is_valid():
		buy_obj = form.save(commit=False)
		buy_obj.wallet = holder
		buy_obj.coin = coin
		buy_obj.save()
		return redirect(reverse('wallets:wallets'))

	context = {
		'coin': coin,
		'form': form,
	}

	return render(request, 'coins/coin.html', context=context)