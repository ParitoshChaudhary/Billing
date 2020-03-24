from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    context = {
        'welcome_msg' : 'Welcome to the Restaurant Application'
    }
    return render(request, 'home.html', context)


def login(request):
    context = {
        'login_msg' : 'Welcome to the Login page'
    }
    return render(request, 'login.html', context)


def register(request):
    context = {
        'register' : 'This is registration page'
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
