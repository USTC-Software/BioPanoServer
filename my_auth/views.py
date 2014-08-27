__author__ = 'feiyicheng'
from django.shortcuts import  HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.base import View
from social_auth.exceptions import AuthFailed
from social_auth.views import complete


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


# login/logout using Google OAuth
class AuthComplete(View):
    def get(self, request, *args, **kwargs):
        backend = kwargs.pop('backend')
        try:
            return complete(request, backend, *args, **kwargs)
        except AuthFailed:
            messages.error(request, "Your Google Apps domain isn't authorized for this app")
            return HttpResponseRedirect(reverse('login'))


class LoginError(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=401)

