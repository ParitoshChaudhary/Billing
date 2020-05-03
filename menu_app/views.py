from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from menu_app.models import Item as ItemList, Category, Cuisine
from menu_app.forms import ItemForm, CategoryForm, CuisineForm
from django.contrib import messages
from django.core.paginator import Paginator
from menu_app.filters import ItemFilter


# Create your views here.
billItemList = []
@login_required(login_url='login')
def menu_list(request):
    print(request.user)
    item_list = ItemList.objects.filter(added_by=request.user)
    category = Category.objects.filter(added_by=request.user)
    cuisine = Cuisine.objects.filter(added_by=request.user)

    filter = ItemFilter(request.GET, queryset = item_list)
    item_list = filter.qs

    paginator = Paginator(item_list, 10)
    page = request.GET.get('pg')
    item_list = paginator.get_page(page)

    context = {
        'items': item_list,
        'category': category,
        'cuisine': cuisine,
        'filter' : filter
    }
    return render(request, 'menu_list.html', context)


@login_required(login_url='login')
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

            if catform.is_valid():
                print('======== CAT FORM IS VALID')

            sorted_cuisines = Cuisine.objects.filter(added_by=request.user)
            sorted_category = Category.objects.filter(added_by=request.user)
            # item.cuisine = Cuisine.objects.filter(cuisine=cui)
            # item.category = Category.objects.filter(category_type=cat)
            item.cuisine = sorted_cuisines.get(cuisine=cui)
            item.category = sorted_category.get(category_type=cat)
            item.name = request.POST.get('name')
            item.cost = request.POST.get('cost')
            item.added_by = request.user
            item.save()

            messages.success(request, 'Item added successfully!!')
        else:
            messages.warning(request, 'Unable to add the item.')
        return redirect('add_item')

    else:
        print(request.user)
        item_list = ItemList.objects.filter(added_by=request.user)
        cuisine = Cuisine.objects.filter(added_by=request.user)
        categories = Category.objects.filter(added_by=request.user)
        paginator = Paginator(item_list, 10)
        page = request.GET.get('pg')
        items = paginator.get_page(page)
        context = {
            'items': items,
            'categories' : categories,
            'cuisine' : cuisine
        }
        return render(request, 'add_item.html', context)


@login_required(login_url='login')
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

            sorted_cuisines = Cuisine.objects.filter(added_by=request.user)
            sorted_category = Category.objects.filter(added_by=request.user)
            # item.cuisine = Cuisine.objects.filter(cuisine=cui)
            # item.category = Category.objects.filter(category_type=cat)
            item.cuisine = sorted_cuisines.get(cuisine=cui)
            item.category = sorted_category.get(category_type=cat)
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


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        cat_form = CategoryForm(request.POST or None)
        if cat_form.is_valid():
            cat = cat_form.save(commit=False)
            cat.added_by = request.user
            cat.save()
            messages.success(request, 'Category added successfully.')
            return redirect('add_category')
        else:
            messages.error(request, 'Unable to add category. Please try again')
            return redirect('add_category')

    else:
        categories = Category.objects.filter(added_by=request.user)
        context = {
            'categories' : categories
        }
        return render(request, 'add_category.html', context)


@login_required(login_url='login')
def add_cuisine(request):
    if request.method == 'POST':
        cuiform = CuisineForm(request.POST or None)
        if cuiform.is_valid():
            cui = cuiform.save(commit=False)
            cui.added_by = request.user
            cui.save()
            messages.success(request, 'Cuisine added successfully.')
            return redirect('add_cuisine')
    else:
        cuisines = Cuisine.objects.filter(added_by=request.user)
        context = {
            'cuisines' : cuisines
        }
        return render(request, 'add_cuisine.html', context)


@login_required(login_url='login')
def delete_item(request, item_id):
    item = ItemList.objects.get(pk=item_id)
    item.delete()
    return redirect('add_item')


@login_required(login_url='login')
def add_item_to_bill(request, item_id):
    global billItemList
    item = ItemList.objects.get(pk=item_id)
    print(type(item))
    billItemList.append(item)
    context = {
        'bill_list' : billItemList
    }
    print(billItemList)
    return render(request, 'menu_list.html', context)


@login_required(login_url='login')
def delete_item_from_bill(request, item_name):
    global billItemList
    for item in billItemList:
        if item.name == item_name:
            billItemList.remove(item)
    return redirect('menu_list')


@login_required(login_url='login')
def generate_bill(request):
    global billItemList
    context = {
        'bill_list' : billItemList
    }
    print(billItemList)
    return render(request, 'bill.html', context)


@login_required(login_url='login')
def get_cost(request):
    cost = []
    if len(billItemList):
        for item in billItemList:
            cost.append(item.cost)
        print(cost)
        total = sum(cost)
        print(total)
        context = {
            'total_amt' : total
        }
    return render(request, 'bill.html', context)
