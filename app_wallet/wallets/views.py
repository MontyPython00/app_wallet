from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from wallets.models import Wallet
from wallets.forms import CreateWalletForm

# Create your views here.


@login_required
def user_wallets_view(request):
	wallets = Wallet.objects.filter(user=request.user.id) # sproboj napisac to na modelu
	context = {
		'wallets': wallets,
	}

	return render(request, 'wallets/user_wallets.html', context=context)


@login_required
def wallet_view(request, wallet_id):
	wallet = get_object_or_404(Wallet, id=wallet_id)
	context = {
		'wallet': wallet
	} 
	print(wallet)
	if request.POST.get('delete') != None:
		wallet.delete()
		return redirect(reverse('wallets:wallets'))

	return render(request, 'wallets/wallet.html', context=context)

@login_required
def create_view(request):
	form = CreateWalletForm(request.POST or None)

	
	if form.is_valid():
		obj = form.save(commit=False)
		obj.user = request.user
		obj.save()
		return redirect(obj)

	context = {
		'form': form
	}

	return render(request, 'wallets/create.html', context=context)


