from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import RegistrationForm
from .models import Problem


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


def problem(request, pk):
    item = Problem.objects.get(title=pk)
    return render(request, 'problem.html', {'problem': item})


def problem_set(request, problem_type):
    problems = Problem.objects.all() if problem_type == 'all' else Problem.objects.filter(type_id=problem_type)
    problem_set_paginator = Paginator(problems, 25)
    page = request.GET.get('page')
    problems = problem_set_paginator.get_page(page)
    return render(request, 'problem_set.html', {'problems': problems, 'problem_type': problem_type})
