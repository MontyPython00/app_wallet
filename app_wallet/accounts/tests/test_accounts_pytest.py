import pytest
from django.urls import reverse
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db

def test_create_account_success(client):
	client_url = reverse('accounts:create')
	data = {
		'username': 'test',
		'email': 'test@domain.pl',
		'password1': 'myPassword123',
		'password2': 'myPassword123',
	}
	response = client.post(path=client_url, data=data)
	user = User.objects.all().first()
	assert response.status_code == 302 # redirected to another page - valid data
	assert User.objects.all().count() == 1
	assert user.username == data.get('username')
	assert user.email == data.get('email')
	


def test_login_success(client):
	client_url = reverse('accounts:login')
	user = User.objects.create_user(username='test123', password='Password123', email='test@domain.pl')
	data = {
		'username': 'test123',
		'password': 'Password123'
	}
	response = client.post(path=client_url, data=data)

	assert response.status_code == 302 # redirected to another page - valid data
	assert User.objects.all().first().username == data.get('username')
	assert User.objects.all().first().email == 'test@domain.pl'


def test_login_failed(client):
	client_url = reverse('accounts:login')
	user = User.objects.create_user(username='test123', password='Password123', email='test@domain.pl')
	data = {
		'username': 'test123',
		'password': 'Password12'
	}
	response = client.post(path=client_url, data=data)

	assert response.status_code == 200
	assert User.objects.all().count() == 1
	assert User.objects.all().first().password != data.get('password')
