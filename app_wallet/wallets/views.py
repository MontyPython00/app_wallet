from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

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

	return render(request, 'wallets/wallet.html', context=context)

@login_required
def create_view(request):
	form = CreateWalletForm(request.POST or None)

	
	if form.is_valid():
		new_form = form.save(commit=False)
		new_form.user = request.user
		new_form.save()

	context = {
		'form': form
	}

	return render(request, 'wallets/create.html', context=context)

