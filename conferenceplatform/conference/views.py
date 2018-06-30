from django.shortcuts import render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from account.models import *
from .models import *
import datetime

def add_conference_(org_user, title, subject, intro, 
                    soliciting_req, paper_temp, register_req,
                    start_accept_time, stop_accept_time, register_start_time, 
                    conference_start_time, conference_end_time):
    pass


def add_conference(request):
    assert request.method == 'POST'
    
    if request.user.has_perm('account.OrganizationUser_Permission'):
        org = request.user.organizationuser
    elif request.user.has_perm('account.OrganizationSubUser_Permission'):
        org = request.user.organizationsubuser.organization
    else:
        return JsonResponse({'message': 'permission denied'})

    try:
        Conference.objects.create(
            origanization=org, title=request.POST['title'], subject=request.POST['subject'],
            introduction=request.POST['introduction'], 
            soliciting_requirement=request.POST['soliciting_requirement'],
            paper_template=request.POST['paper_template'], 
            register_requirement=request.POST['register_requirement'],
            accept_start=datetime.strptime(request.POST['accept_start']),
            accept_due=datetime.strptime(request.POST['accept_due']),
            modify_due=datetime.strptime(request.POST['modify_due']),
            register_start=datetime.strptime(request.POST['register_start']),
            conference_start=datetime.strptime(request.POST['conference_start']),
            conference_due=datetime.strptime(request.POST['conference_due']),
        )
        return JsonResponse({'message': 'success'})
    except MultiValueDictKeyError:
        return JsonResponse({'message': 'insufficient data'})
    except ValueError:
        return JsonResponse({'message': 'invalid datetime format'})
    
