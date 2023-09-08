from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from coins.forms import BuyForm, SellForm
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
	holder = Wallet.objects.get(main_wallet__user=request.user, active=True)	#AS DEFAULT NONE WALLET IS ACTIVE DEAL WITH IT 
	form = BuyForm(request.POST or None, coin_identifier=coin_id, wallet=holder)
	form2 = SellForm(request.POST or None)
	if form.is_valid():
		buy_obj = form.save(commit=False)
		buy_obj.wallet = holder
		buy_obj.coin = coin
		buy_obj.save()
		return redirect(coin)
	elif form2.is_valid():
		sell_obj = form2.save(commit=False)
		sell_obj.wallet =holder
		sell_obj.coin = coin
		sell_obj.save()
		return redirect(coin)
	context = {
		'coin': coin,
		'form': form,
		'form2': form2,
	}

	return render(request, 'coins/coin.html', context=context)