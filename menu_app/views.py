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
        'items': item_list
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


def calculate_state_tax(price):
    state_tax = .09
    return price * state_tax


def calculate_country_tax(price):
    country_tax = .09
    return price * country_tax


@login_required(login_url='login')
def get_cost(request):
    cost = []
    if len(billItemList):
        for item in billItemList:
            cost.append(item.cost)
        print(cost)
        if request.user.profile.add_tax:
            sum_cost = sum(cost)
            state_tax = calculate_state_tax(sum_cost)
            country_tax = calculate_country_tax(sum_cost)
            total = sum_cost + state_tax + country_tax
            context = {
            'total_amt' : total,
            'base_cost' : sum_cost
            }
            
        else:
            sum_cost = sum(cost)
            state_tax = calculate_state_tax(sum_cost)
            country_tax = calculate_country_tax(sum_cost)
            base_cost = sum_cost - (state_tax + country_tax)
            context = {
                'total_amt' : sum_cost,
                'base_cost' : base_cost
            }
    
    return render(request, 'bill.html', context)


def is_valid_query_param(param):
    return param != '' and param is not None
    

def search_name(request):
    qs = ItemList.objects.filter(added_by=request.user)
    categories = Category.objects.filter(added_by=request.user)
    item_name = request.GET.get("item_name")
    category_type = request.GET.get("category_type")

    if is_valid_query_param(item_name):
        qs = qs.filter(name__icontains = item_name)

    # if is_valid_query_param(category_type) and category_type != 'Choose...':
    #     qs = qs.get(Item__category__icontains=category_type)
    #     print(qs)

    context = {
            'items' : qs
    }
    return render(request, 'menu_list.html', context)
