from django.urls import path
from bills_app import views

urlpatterns = [
    path('', views.view_all_bills, name='bills')
]
