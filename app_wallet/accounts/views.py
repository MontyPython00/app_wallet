from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from accounts.forms import CreateAccountForm, LoginForm
from django.urls import reverse
# Create your views here.



def create_view(request):
	form = CreateAccountForm(request.POST or None)
	context = {
		'form': form
	}

	if form.is_valid():
		form.save()
		return redirect(reverse('wallets:create'))

	return render(request, 'accounts/create.html', context)


def login_view(request):
	if request.method == 'POST':

		form = LoginForm(request, data=request.POST)
		if form.is_valid():
			user_data = form.cleaned_data
			user = authenticate(request, username=user_data.get('username'), password=user_data.get('password'))
			login(request, user)
			return redirect(reverse('wallets:wallets'))
	
	else:
		form = LoginForm(request)

	context = {
		'form': form
	}
	return render(request, 'accounts/login.html', context=context)
	
def logout_view(request):
	if request.method == 'POST':
		logout(request)
		return redirect(reverse('accounts:login'))
	else:
		return render(request, 'accounts/logout.html', context=None)