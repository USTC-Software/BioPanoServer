__author__ = 'feiyicheng'
from django.shortcuts import render_to_response, HttpResponse
# from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


# login to LDAP server ## cache: save for 1 hour
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        print username, password

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            state = "Valid account"
        else:
            state = "Inactive account"
        return HttpResponse(state)
    if request.method == "GET":
        state = ""
        username = ""
        return render_to_response('login.html', RequestContext(request, {'state': state, 'username': username}))


#logout
@login_required
def logout_view(request):
    logout(request)
    return HttpResponse('<html><body>logging out...<br>logout successfully</body></html>')



