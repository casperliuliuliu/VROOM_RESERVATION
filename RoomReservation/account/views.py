from django.shortcuts import render, redirect
from .forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as login_, authenticate, logout as logout_


# Create your views here.
def login(request):
	if request.method == 'POST':
		return login_post(request)
	return render(request, 'account/login.html', {
		'form': AuthenticationForm()
	})

def login_post(request):
	form = AuthenticationForm(request, request.POST)


	if(form.is_valid()):
		user = form.get_user()
		login_(request, user)

		return redirect('room_index')
	return render(request, 'account/login.html', {
		'form': form
	})
 
def register(request):
	if request.method == 'POST':
		return register_post(request)
	return render(request, 'account/register.html',
		{
			'form': UserCreationForm()
		})

def register_post(request):
	form = UserCreationForm(request.POST)
	if form.is_valid():
		user = form.save()
		return redirect('account_login')
	
	return render(request, 'account/register.html',
	{
		'form': form
	})
	
def logout(request):
	if request.method == 'POST':
		logout_(request)
		return redirect('room_index')