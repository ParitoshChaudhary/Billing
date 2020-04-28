from django.http import HttpResponse
from django.shortcuts import redirect

def check_authentication(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('menu_list')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function
