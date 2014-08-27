__author__ = 'feiyicheng'
from django.shortcuts import  HttpResponse
# from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# login to LDAP server ## cache: save for 1 hour
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        print username, password

        user = authenticate(username=username, password=password)
        if user is not None:
            # authenticate succeed
            login(request, user)
            return HttpResponse("{'status':'success'}")
        else:
            # authenticate failed
            return HttpResponse("{'status':'error','reason':'username and password do not match'}")


    if request.method == "GET":
        # not using method POST
        return HttpResponse("{'status':'error','reason':'pls use POST method'}")


#logout
@login_required
def logout_view(request):
    logout(request)
    return HttpResponse("{'status':'success'}")



