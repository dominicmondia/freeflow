from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created!')

            return redirect('login')

    context = {'form': form}
    return render(request, 'signup.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password incorrect')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('home')
