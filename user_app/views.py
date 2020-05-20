from django.shortcuts import render, redirect
from django.http import HttpResponse
from user_app.forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from menu_app.decorators import check_authentication
from django.contrib.auth.decorators import login_required


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


@login_required(login_url='login')
def profile(request):
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    
    return render(request, 'profile.html', context)


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
