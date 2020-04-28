from django.shortcuts import render, redirect
from django.http import HttpResponse
from user_app.forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from menu_app.decorators import check_authentication


# Create your views here.
def home(request):
    context = {
        'welcome_msg' : 'Welcome to the Restaurant Application'
    }
    return render(request, 'home.html', context)

@check_authentication
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('menu_list')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    context = {
        'login_msg' : 'Welcome to the Login page'
    }
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@check_authentication
def registerUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Profile created successfully for user ' + user.upper())
    else:
        form = RegisterForm()
    context = {
        'form' : form
    }
    return render(request, 'register.html', context)


def contact(request):
    context = {
        'contact_msg' : 'Welcome to the Contact Page'
    }
    return render(request, 'contact.html', context)


def about(request):
    context = {
        'about_msg' : 'Welcome to the About Page'
    }
    return render(request, 'about.html', context)
