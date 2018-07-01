from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse
from .models import *
from .forms import *
from .normal_user_views import *
from .organization_user_views import *
from .admin_user_views import *
from .organization_sub_user_views import *

# Create your views here.

def user_login(request):
    data = {'message':'', 'data':{}}    
    assert request.method == 'POST'
    login_form = LoginForm(request.POST)
    if login_form.is_valid() is False:
        data['message'] = 'format error'
        return JsonResponse(data, safe=False)
    
    username = login_form.cleaned_data['username']
    password = login_form.cleaned_data['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        data['message'] = 'success'
        if user.has_perm('account.NormalUser_Permission'):
            data['data']['user_type'] = 'normal_user'
        elif user.has_perm('account.OrganizationUser_Permission'):
            data['data']['user_type'] = 'organization_user'
        elif user.has_perm('account.OrganizationSubUser_Permission'):
            data['data']['user_type'] = 'organization_sub_user'
        else:
            data['data']['user_type'] = 'our_admin'
        login(request, user)
    else:
        data['message'] = 'username or password error'
    return JsonResponse(data, safe=False)

def change_password(request):
    data = {'message':'', 'data':{}}
    assert request.method == 'POST'
    change_password_form = ChangePasswordForm(request.POST)
    if change_password_form.is_valid() is False:
        data['message'] = 'format error'
        return JsonResponse(data, safe=False)
    
    username = change_password_form.cleaned_data['username']
    old_password = change_password_form.cleaned_data['old_password']
    new_password = change_password_form.cleaned_data['new_password']
    confirm_password = change_password_form.cleaned_data['confirm_password']
    user = authenticate(request, username=username, password=old_password)
    if user is not None:
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            data['message'] = 'success'
        else:
            data['message'] = 'new_password error'
    else:
        data['message'] = 'old_password error'
    
    return JsonResponse(data, safe=True)

def user_logout(request):
    data = {'message':'', 'data':{}}
    logout(request)
    data['message'] = 'success'
    return JsonResponse(data)

def user_type(request):
    data = {'message':'', 'data':{}}
    user = request.user
    if user is None:
        data['message'] = 'anonymous user'
        return JsonResponse(data)
    
    data['message'] = 'success'
    if user.has_perm('account.NormalUser_Permission'):
        data['data']['user_type'] = 'normal_user'
    elif user.has_perm('account.OrganizationUser_Permission'):
        data['data']['user_type'] = 'organization_user'
    elif user.has_perm('account.OrganizationSubUser_Permission'):
        data['data']['user_type'] = 'organization_sub_user'
    else:
        data['data']['user_type'] = 'our_admin'
    return JsonResponse(data)
    