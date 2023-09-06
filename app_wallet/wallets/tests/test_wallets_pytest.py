import pytest
from wallets.models import Wallet, MainWallet
from django.contrib.auth.models import User
from django.urls import reverse
from wallets.forms import CreateWalletForm, UpdateWalletForm

pytestmark = pytest.mark.django_db


# #Test Validators ---> Is_active, Unique_name, Create_wallet

# def test_create_wallet_success():
# 	user = User.objects.create_user(username='test', password='myPassword123')
# 	main_wallet = MainWallet.objects.get(user=user)
# 	data = {
# 		'name': 'TestWallet',
# 		'main_wallet': main_wallet,
# 		'wallet_id': '123121'
# 	}
# 	wallet = Wallet.objects.create(**data)
# 	assert Wallet.objects.all().count() == 1
# 	assert wallet.name == data.get('name')
# 	assert wallet.wallet_id == data.get('wallet_id')


# #Test valid only for update_form regarding to if case where condition is self.id has to exist 
# def test_unique_name_update_model_success():
# 	user = User.objects.create_user(username='test', password='myPassword123')
# 	main_wallet = MainWallet.objects.get(user=user)
# 	data1 = {
# 		'name': 'TestWallet1',
# 		'main_wallet': main_wallet,
# 		'wallet_id': 'asdaa'
# 	}
# 	data2 = {
# 		'name': 'TestWallet2',
# 		'main_wallet': main_wallet,
# 		'wallet_id': '123121'
# 	}

# 	wallet1 = Wallet.objects.create(**data1)
# 	wallet2 = Wallet.objects.create(**data2)
# 	Wallet.objects.get(pk=1).name = data2.get('name')

# 	assert Wallet.objects.all().count() == 2
# 	assert wallet1.name != data2.get('name')
# 	assert wallet1.wallet_id == data1.get('wallet_id')
# 	assert wallet2.wallet_id == data2.get('wallet_id')


# #Test valid only for create_form; validation is passed to forms.py
# @pytest.mark.parametrize("name, wallet_id", [('tes', 'asda'), ('test12', 'asdaas'), ('test1234','asdadsa')])
# def test_create_wallet_form_success(name, wallet_id):
# 	user = User.objects.create_user(username='test', password='myPassword123')
# 	main_wallet = MainWallet.objects.get(user=user)
# 	data = {
# 		'name': 'test123',
# 		'wallet_id': 'asdas',
# 		'main_wallet': main_wallet,
# 		'user_experience': 'FRESH'
# 	}
# 	Wallet.objects.create(**data)
# 	data2 = {
# 		'name': name,
# 		'wallet_id': wallet_id,
# 		'main_wallet': main_wallet,
# 		'user_experience': 'FRESH'
# 	}
# 	form = CreateWalletForm(data2, user=user)
	
	
# 	is_form_correct = form.is_valid()
# 	assert is_form_correct == True
# 	assert form.cleaned_data['name'] == data2.get('name')




# def test_create_wallet_form_failed():
# 	user = User.objects.create_user(username='test', password='myPassword123')
# 	main_wallet = MainWallet.objects.get(user=user)
# 	wallet_data = {
# 		'name': 'test123',
# 		'wallet_id': 'asdas',
# 		'main_wallet': main_wallet,
# 		'user_experience': 'FRESH'
# 	}
# 	Wallet.objects.create(**wallet_data)
# 	wallet_data2 = {
# 		'name': 'test123',
# 		'wallet_id': 'asdasasd',
# 		'main_wallet': main_wallet,
# 		'user_experience': 'FRESH'
# 	}
# 	form = CreateWalletForm(wallet_data2, user=user)
	
	
# 	is_form_correct = form.is_valid()
# 	assert is_form_correct == False
# 	assert form.cleaned_data['name'] == wallet_data2.get('name')



# def test_active_wallet_success():
# 	user = User.objects.create_user(username='test', password='myPassword123')
# 	main_wallet = MainWallet.objects.get(pk=1)
# 	wallet_data1 = {
# 		'name': 'test123',
# 		'wallet_id': 'wallet',
# 		'main_wallet': main_wallet,
# 		'user_experience': 'FRESH',
# 		'active': False
# 	}
# 	wallet_data2 = {
# 		'name': 'test12345',
# 		'wallet_id': 'wallet123',
# 		'main_wallet': main_wallet,
# 		'user_experience': 'FRESH',
# 		'active': False
# 	}
# 	wallet1 = Wallet.objects.create(**wallet_data1)
# 	wallet2 = Wallet.objects.create(**wallet_data2)
# 	wallet2_update = {
# 		'name': 'test12345',
# 		'wallet_id': 'wallet123',
# 		'user_experience': 'FRESH',
# 		'active': True
# 	}
# 	form = UpdateWalletForm(wallet2_update, instance=wallet2)
# 	is_form_valid = form.is_valid()
# 	assert Wallet.objects.all().count() == 2
# 	assert is_form_valid == True


# def test_active_wallet_failed():
# 	user = User.objects.create_user(username='test', password='myPassword123')
# 	main_wallet = MainWallet.objects.get(pk=1)
# 	wallet_data1 = {
# 		'name': 'test123',
# 		'wallet_id': 'wallet',
# 		'main_wallet': main_wallet,
# 		'user_experience': 'FRESH',
# 		'active': True
# 	}
# 	wallet_data2 = {
# 		'name': 'test12345',
# 		'wallet_id': 'wallet123',
# 		'main_wallet': main_wallet,
# 		'user_experience': 'FRESH',
# 		'active': False
# 	}
# 	wallet1 = Wallet.objects.create(**wallet_data1)
# 	wallet2 = Wallet.objects.create(**wallet_data2)
# 	wallet2_update = {
# 		'name': 'test12345',
# 		'wallet_id': 'wallet123',
# 		'user_experience': 'FRESH',
# 		'active': True
# 	}
# 	form = UpdateWalletForm(wallet2_update, instance=wallet2)
# 	is_form_valid = form.is_valid()
# 	assert Wallet.objects.all().count() == 2
# 	assert is_form_valid == False