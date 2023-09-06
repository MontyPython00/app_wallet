from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ValidationError

from wallets.models import Wallet, MainWallet
from wallets.forms import CreateWalletForm, UpdateWalletForm
from coins.models import Coin

# Create your views here.


@login_required
def user_wallets_view(request):
	wallets = Wallet.objects.filter(main_wallet__user=request.user.id) # sproboj napisac to na modelu
	context = {
		'wallets': wallets,
	}

	return render(request, 'wallets/user_wallets.html', context=context)


@login_required
def wallet_view(request, wallet_id):
	wallet = get_object_or_404(Wallet, id=wallet_id)
	coins = Coin.objects.filter(holders=wallet)
	context = {
		'wallet': wallet,
		'coins': coins
	} 
	if request.POST.get('delete') != None:
		wallet.delete()
		return redirect(reverse('wallets:wallets'))

	return render(request, 'wallets/wallet.html', context=context)

@login_required
def create_view(request):
	
	form = CreateWalletForm(request.POST or None, user=request.user)
	main_wallet = MainWallet.objects.get(user=request.user)

	if form.is_valid():
		obj = form.save(commit=False) 
		obj.main_wallet = main_wallet
		obj.save()
		return redirect(obj) # redirect use get_absolute_url written in model

	context = {
		'form': form
	}

	return render(request, 'wallets/create.html', context=context)


@login_required
def update_view(request, wallet_id):
	wallet = get_object_or_404(Wallet, id=wallet_id)
	form = UpdateWalletForm(request.POST or None, instance=wallet)
	context = {
		'form': form,
	}
	if form.is_valid():
		form.save()
		return redirect(wallet)
	return render(request, 'wallets/update.html', context=context)


