from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.db.transaction import atomic, DatabaseError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .forms import *
from .decorators import user_has_permission


@user_has_permission('account.AdminUser_Permission')
def accept_orgnization_register(request):
    assert request.method == 'POST'
    data = {'message' :''}
    form = AcceptorgregForm(request.POST)
    if form.is_valid() is False:
        data['message'] = 'format error'
        return JsonResponse(data)
    org_pk = form.cleaned_data['org_pk']
    
    org = OrganizationUser.objects.filter(pk = org_pk)
    if len(org) == 0:
        data['message'] = 'organization not exist'
        return JsonResponse(data)
    
    org_user = org[0].user
    org_user.is_active = True
    org_user.save()
    data['message'] = 'success'
    return JsonResponse(data)
