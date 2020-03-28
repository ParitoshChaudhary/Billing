import django_filters
from menu_app.models import *


class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['cost']
