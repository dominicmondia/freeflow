from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator

from .forms import RegistrationForm
from .models import Problem

import sympy as sp
from sympy.parsing.latex import parse_latex
import pint


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

    def is_equal(expr1, expr2):
        def latex_parser(expr):
            expr = expr.lower()
            wrappers = ['(', ')', '[', ']']
            if ',' in expr and not any(wrapper in expr for wrapper in wrappers):
                expr_list = expr.split(',')
                updated_expr_list = []
                for term in expr_list:
                    term = str(latex_parser(term))
                    updated_expr_list.append(term)
                expr = ','.join(updated_expr_list)
                return expr

            elif '\cup' in expr:
                expr_list = expr.split('\cup')
                updated_expr_list = []
                for term in expr_list:
                    term = str(latex_parser(term))
                    updated_expr_list.append(term)
                expr = '\cup'.join(updated_expr_list)

            elif ',' in expr:
                affix = [expr[0], expr[-1]]
                expr = expr[1:len(expr) - 1]
                expr = str(latex_parser(expr))
                expr = affix[0] + expr + affix[1]
                return expr

            try:
                return parse_latex(expr)
            except sp.parsing.latex.errors.LaTeXParsingError:
                return expr

        def evaluate_expression(expr):
            units_reg = pint.get_application_registry()
            try:
                units_expr = units_reg.parse_expression(expr)
                return units_expr.magnitude, units_expr.units

            except AttributeError:
                expr = expr.split(r'\text{')
                magnitude = latex_parser(expr[0])
                expr = expr[-1][:-1] if len(expr) > 1 else expr[0]

                try:
                    units = units_reg.parse_units(expr)
                except pint.errors.UndefinedUnitError:
                    units = None
                except ValueError:
                    units = None
                except TypeError:
                    units = None

                return magnitude, units

            except:
                return 0, None

        mag1, units1 = evaluate_expression(expr1)
        mag2, units2 = evaluate_expression(expr2)

        if type(mag1) == str or type(mag2) == str:
            return mag1.replace(' ', '').lower() == mag2.replace(' ', '').lower() and units1 == units2
        else:
            # print(mag1, units1, mag2, units2)
            return sp.simplify(mag1 - mag2) == 0 and units1 == units2

    if request.method == 'POST':
        user_answer = request.POST.get('user_answer')
        correct_answer = item.answer
        if is_equal(user_answer, correct_answer):
            messages.info(request, "correct")
        else:
            messages.info(request, "incorrect")
            messages.info(request, is_equal(user_answer, correct_answer))
        messages.info(request, "attempted")
        return redirect(f'/problem/{pk}')
    return render(request, 'problem.html', {'problem': item})


def problem_set(request, problem_type):
    problems = Problem.objects.all() if problem_type == 'all' else Problem.objects.filter(type_id=problem_type)
    problem_set_paginator = Paginator(problems, 20)
    page = request.GET.get('page')
    problems = problem_set_paginator.get_page(page)
    return render(request, 'problem_set.html', {'problems': problems, 'problem_type': problem_type})
