from django.shortcuts import render, redirect
from .forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as login_, logout as logout_
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
@user_passes_test(lambda u: not u.is_authenticated, login_url='room_index')
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

		try:
			redirect_to = request.GET["next"]
		except KeyError:
			redirect_to = "room_index"
		return redirect(redirect_to)	
		
	return render(request, 'account/login.html', {
		'form': form
	})
 
@user_passes_test(lambda u: not u.is_authenticated, login_url='room_index')
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
	
@login_required
def logout(request):
	if request.method == 'POST':
		logout_(request)
		return redirect('room_index')
	return redirect('room_index')