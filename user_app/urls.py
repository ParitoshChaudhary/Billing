from django.urls import path
from user_app import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', views.loginUser, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.registerUser, name='register'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
] 

admin.autodiscover()