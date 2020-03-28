from django import forms
from menu_app.models import Item, Category, Cuisine


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'cost']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_type']

class CuisineForm(forms.ModelForm):
    class Meta:
        model = Cuisine
        fields = ['cuisine']
