from django.contrib import admin
from menu_app.models import Item as Item_list, Cuisine, Category

# Register your models here.
class ItemListAdmin(admin.ModelAdmin):
    search_fields = ('name', 'added_by')


admin.site.register(Item_list)
admin.site.register(Cuisine)
admin.site.register(Category)
