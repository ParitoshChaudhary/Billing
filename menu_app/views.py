from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from menu_app.models import Item as ItemList, Category, Cuisine
from menu_app.forms import ItemForm, CategoryForm, CuisineForm
from django.contrib import messages
from django.core.paginator import Paginator


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
    paginator = Paginator(item_list, 10)
    page = request.GET.get('pg')
    item_list = paginator.get_page(page)
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
        paginator = Paginator(item_list, 10)
        page = request.GET.get('pg')
        items = paginator.get_page(page)
        context = {
            'items': items,
            'categories' : categories,
            'cuisine' : cuisine
        }
        return render(request, 'add_item.html', context)


def edit_item(request, item_id):
    if request.method == 'POST':
        item = ItemList.objects.get(pk=item_id)
        itemform = ItemForm(request.POST, instance = item)
        cuisineform = CuisineForm(request.POST, instance = item.cuisine)
        catform = CategoryForm(request.POST, instance = item.category)
        if itemform.is_valid():
            item = itemform.save(commit=False)
            cui = cuisineform.save(commit=False)
            cat = catform.save(commit=False)

            item.cuisine = Cuisine.objects.get(cuisine=cui)
            item.category = Category.objects.get(category_type=cat)
            item.name = request.POST.get('name')
            item.cost = request.POST.get('cost')
            item.save()
        messages.success(request, 'Item edited successfully.')
        return redirect('add_item')

    else:
        item_name = ItemList.objects.get(pk=item_id)
        cuisine = Cuisine.objects.all()
        categories = Category.objects.all()
        context = {
            'items': item_name,
            'categories' : categories,
            'cuisine' : cuisine
        }
        return render(request, 'edit.html', context)


def delete_item(request, item_id):
    item = ItemList.objects.get(pk=item_id)
    item.delete()
    return redirect('add_item')
