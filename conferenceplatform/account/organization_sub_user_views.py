from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.db.transaction import atomic, DatabaseError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .forms import *
from .decorators import *

#这里是需要OrganizationUser登录才能使用的

@user_has_permission('account.OrganizationUser_Permission')
def organization_sub_user_register(request):
    

    assert request.method == 'POST'
    data = {'message':'', 'data':{}}
    form = OrganizationSubUserForm(request.POST)
    if form.is_valid() is False:
        data['message'] = 'format error'
        return JsonResponse(data)
    
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    confirm_password = form.cleaned_data['confirm_password']


    if password != confirm_password:
        data['message'] = 'password error'
        return JsonResponse(data, safe=False)
    search_user = User.objects.filter(username = username)
    if len(search_user) != 0:
        data['message'] = 'username error'
        return JsonResponse(data, safe=False)
    
    try:
        with atomic():
            new_user = User.objects.create_user(username, email=username, password=password)
            content_type = ContentType.objects.get_for_model(User_Permission)
            permission = Permission.objects.get(content_type=content_type,codename='OrganizationSubUser_Permission')
            permission2 = Permission.objects.get(content_type=content_type, codename='ConferenceRelated_Permission')
            new_user.save()
            new_user.user_permissions.add(permission, permission2)
            organization_sub_user = OrganizationSubUser(
                user = new_user,
                organization = request.user.organizationuser
            )
            data['message'] = 'success'
    except DatabaseError:
        data['message'] = 'database error'
    
    return JsonResponse(data, safe=False)
