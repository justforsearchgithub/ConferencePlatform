from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import *
from .normal_user_views import *
from .organization_user_views import *
from .admin_user_views import *
# Create your views here.

def user_login(request):
    assert request.method == 'POST'
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.has_perm('account.NormalUser_Permission'):
            normaluser = NormalUser.objects.get(user=user)
            #return normaluser json data
        elif user.has_perm('account.OrganizationUser_Permission'):
            organizationuser = OrganizationUser.objects.get(user=user)
            #
        elif user.has_perm('account.OrganizationSubUser_Permission'):
            organizationsubuser = OrganizationUser.objects.get(user=user)
            #
        else:
            ouradmin = OurAdmin.objects.get(user=user)
            #
    else:
        #return error message json data
        return
