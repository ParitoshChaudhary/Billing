from django.urls import path
from menu_app import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('additem/', views.add_item, name='add_item'),
    path('delete/<item_id>', views.delete_item, name='delete_item'),
    path('addtobill/<item_id>', views.add_item_to_bill, name='add_item_to_bill'),
    path('edit/<item_id>', views.edit_item, name='edit_item')
]
