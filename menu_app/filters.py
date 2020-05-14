import django_filters
from django_filters import CharFilter
from menu_app.models import *


class ItemFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['cost', 'added_by']
