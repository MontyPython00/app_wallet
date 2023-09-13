from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from coins.forms import BuyForm, SellForm, CreateCoinForm
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
	holder = Wallet.objects.filter(main_wallet__user=request.user, active=True).first()	#AS DEFAULT NONE WALLET IS ACTIVE DEAL WITH IT #IF WALLET DOESNT EXISTS SAME PROBLEM
	form = BuyForm(request.POST or None, coin_identifier_buy=coin_id, wallet_buy=holder)
	form2 = SellForm(request.POST or None, coin_identifier_sell=coin_id, wallet_sell=holder)
	if form.is_valid() and 'BUY' == request.POST.get('action'):

		buy_obj = form.save(commit=False)
		buy_obj.wallet = holder
		buy_obj.coin = coin
		buy_obj.save()
		return redirect(coin)
	elif form2.is_valid() and 'SELL' == request.POST.get('action'):
		sell_obj = form2.save(commit=False)
		sell_obj.wallet = holder
		sell_obj.coin = coin
		sell_obj.save()
		return redirect(coin)

	context = {
		'coin': coin,
		'form': form,
		'form2': form2,
		'wallet_dont_exists': holder == None,
	}

	return render(request, 'coins/coin.html', context=context)



def create_view(request):
	form = CreateCoinForm(request.POST or None)

	if form.is_valid():
		coin_obj = form.save()
		return redirect(coin_obj)

	context = {'form': form,}
	return render(request, 'coins/create.html', context=context)
