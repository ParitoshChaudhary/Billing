from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bills_app.models import Bills

# Create your views here.
@login_required(login_url='login')
def view_all_bills(request):
    bill_list = Bills.objects.filter(generated_by=request.user)
    print(bill_list)
    
    for item in bill_list:
        for i in item.items.all():
            print(i)
    
    context = {
        'bill_list' : bill_list
    }
    
    return render(request, 'bill_list.html', context)