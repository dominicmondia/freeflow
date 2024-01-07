from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .filters import ProblemFilter
from .forms import RegistrationForm, PasswordChangeForm
from .models import Problem, UserProfile, ProblemReport

from sympy import sympify
from sympy.parsing.latex import parse_latex
import re


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


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
    user = request.user
    try:
        titles = request.session["problem_titles"]
    except KeyError:
        titles = request.session["problem_titles"] = [str(title) for title in Problem.objects.all().order_by('id')]

    try:
        prev_problem_title = titles[titles.index(item.title) - 1] if titles.index(item.title) > 0 else None
        next_problem_title = titles[titles.index(item.title) + 1] if titles.index(item.title) < len(
            titles) - 1 else None
    except ValueError:
        titles = request.session["problem_titles"] = [str(title) for title in Problem.objects.all().order_by('id')]
        prev_problem_title = titles[titles.index(item.title) - 1] if titles.index(item.title) > 0 else None
        next_problem_title = titles[titles.index(item.title) + 1] if titles.index(item.title) < len(
            titles) - 1 else None

    def simplify(expr):
        special_chars = ["%", "_"]  # symbols unsupported by sympy.parsing.latex.parse_latex
        affixes = [r"\left(", r"\left[", r"\right)", r"\right]", ","]
        affixes_non_latex = ["(", ")", "[", "]"]

        # if any(affix in expr for affix in affixes):
        if "," in expr:
            """ 
            handles ordered pair, multiple expressions separated by a comma, and intervals
            """

            expr_list = [item.replace(" ", "").replace(r"//", r"/") for item in
                         re.split(r"(\\left\(|\\left\[|\\right\)|\\right]|,)", expr) if
                         item not in ["", ","]]

            expr_list = [item if any(char in special_chars for char in item)
                         else item[-1] if item in affixes
            else sympify(parse_latex(item))
                         for item in expr_list]

            if any(item in expr_list for item in affixes_non_latex):
                return expr_list
            else:
                return sorted(expr_list)

        if any(char in expr for char in special_chars):
            return expr

        return sympify(parse_latex(expr))

    def is_equal(expr1, expr2):
        expr1, expr2 = simplify(expr1), simplify(expr2)
        if type(expr1) is not type(expr2):
            return False

        return str(expr1).replace(" ", "") == str(expr2).replace(" ", "")

    if request.method == 'POST':
        if 'user_answer' in request.POST:
            user_answer = r"{}".format(request.POST.get('user_answer'))
            correct_answer = r"{}".format(item.answer)
            if is_equal(user_answer, correct_answer):
                messages.info(request, "correct")
                status = 's'
            else:
                messages.info(request, "incorrect")
                status = 'a'
            if user.is_authenticated:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.history[item.title] = status
                user_profile.save()
            messages.info(request, "attempted")
            return redirect(f'/problem/{pk}')
        else:
            report = ProblemReport(problem_id=item, description=request.POST.get('description'))
            report.save()
    return render(request, 'problem.html', {'problem': item,
                                            'next_problem_title': next_problem_title,
                                            'prev_problem_title': prev_problem_title})


def problem_set(request, problem_type):
    user = request.user
    problems = Problem.objects.all().order_by('id') if problem_type == 'all' else Problem.objects.filter(
        type=problem_type).order_by('id')

    problem_filter = ProblemFilter(request.GET, queryset=problems)
    problems = problem_filter.qs
    request.session["problem_titles"] = [str(title[0]) for title in problems.values_list('title')]
    problem_set_paginator = Paginator(problems, 20)
    page = request.GET.get('page')

    if user.is_authenticated:
        user_profile = UserProfile.objects.get(user=user)
        user_history = user_profile.history
    else:
        user_history = {}

    problems = problem_set_paginator.get_page(page)

    return render(request,
                  'problem_set.html',
                  {'problems': problems, 'problem_type': problem_type, 'filter': problem_filter,
                   'user_history': user_history})


def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('home')
    user_profile = UserProfile.objects.get(user=user)
    topics = Problem.objects.values_list('type', flat=True).distinct()
    user_statistics = {}

    for topic in topics:
        solved_problems = len([Problem.objects.get(title=problem_title) for problem_title in user_profile.history.keys() if
                               Problem.objects.get(title=problem_title).type == topic and user_profile.history[
                                   problem_title] == 's'])
        total_number_problems = Problem.objects.filter(type=topic).count()
        user_statistics[topic] = {'solved_problems': solved_problems,
                                  'total_number_problems': total_number_problems}
    total = {
        "num_solved_problems": list(user_profile.history.values()).count('s'),
        "num_problems": Problem.objects.all().count()
    }

    return render(request, 'profile.html',
                  {'user_profile': user_profile, 'user_statistics': user_statistics, 'total': total})


def change_username(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'POST':
            new_username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if User.objects.all().filter(username=new_username).exists():
                messages.info(request, f'Username: {new_username} is already in use.')
                return render(request, 'change_username.html')

            if user is not None:
                user.username = new_username
                user.save()
                messages.info(request, 'Username updated successfully.')
                return redirect('change_username')
            else:
                messages.info(request, 'Incorrect password')

        return render(request, 'change_username.html')

    else:
        return redirect('home')


def change_password(request):
    form = PasswordChangeForm(request.user, request.POST)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
