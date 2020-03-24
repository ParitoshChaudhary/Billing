from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from menu_app.models import Item as ItemList, Category, Cuisine
from menu_app.forms import ItemForm, CategoryForm, CuisineForm
from django.contrib import messages


# Create your views here.
@login_required
def menu_list(request):
    item_list = ItemList.objects.all()
    category = Category.objects.all()
    cuisine = Cuisine.objects.all()
    context = {
        'items': item_list,
        'category': category,
        'cuisine': cuisine
    }
    return render(request, 'menu_list.html', context)


@login_required()
def add_item(request):
    if request.method == 'POST':
        print(request.POST)
        itemform = ItemForm(request.POST or None)
        cuisineform = CuisineForm(request.POST or None)
        catform = CategoryForm(request.POST or None)
        if itemform.is_valid():
            item = itemform.save(commit=False)
            cui = cuisineform.save(commit=False)
            cat = catform.save(commit=False)

            item.cuisine = Cuisine.objects.get(cuisine=cui)
            item.category = Category.objects.get(category_type=cat)
            item.name = request.POST.get('name')
            item.cost = request.POST.get('cost')
            item.save()

            messages.success(request, 'Item added successfully!!')
        else:
            messages.warning(request, 'Unable to add the item.')
        return redirect('add_item')

    else:
        item_list = ItemList.objects.all()
        cuisine = Cuisine.objects.all()
        categories = Category.objects.all()
        context = {
            'items': item_list,
            'categories' : categories,
            'cuisine' : cuisine
        }
        return render(request, 'add_item.html', context)


def edit_item(request, item_id):
    if request.method == 'POST':
        pass

    else:
        item_name = ItemList.objects.get(pk=item_id)
        context = {
            'items': item_name
        }
        return render(request, 'edit.html', context)


def delete_item(request, item_id):
    item = ItemList.objects.get(pk=item_id)
    item.delete()
    return redirect('add_item')
