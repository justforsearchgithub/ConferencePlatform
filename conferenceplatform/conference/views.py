from django.shortcuts import render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db import transaction as database_transaction   
from django.utils import timezone
import datetime
import json
from account.models import *
from .models import *
from .forms import *
from .utils import *

from account.decorators import user_has_permission

@user_has_permission('account.ConferenceRelated_Permission')
def add_conference(request):
    assert request.method == 'POST'
    form = ConferenceInfoForm(request.POST, request.FILES)

    if form.is_valid():
        with database_transaction.atomic():
            org = utils.get_organization(request.user)
            assert org is not None
            try:
                subject = Subject.ojbects.get(name=form.cleaned_data['subject'])
            except Subject.DoesNotExist:
                print('BUG: no subject: ' + form.cleaned_data['subject'])

            conf = Conference(
                origanization=org, title=form.cleaned_data['title'], 
                subject=subject,
                introduction=form.cleaned_data['introduction'], 
                soliciting_requirement=form.cleaned_data['soliciting_requirement'],            
                register_requirement=form.cleaned_data['register_requirement'],
                accept_start=timezone.now()
                accept_due=form.cleaned_data['accept_due'],
                # modify_due=form.cleaned_data['modify_due'],
                register_start=form.cleaned_data['register_start'],
                conference_start=form.cleaned_data['conference_start'],
                conference_due=datetime.cleaned_data['conference_due']

                paper_template=form.paper_template
            )
            if not utils.valid_timepoints(conf):
                return JsonResponse({'message': 'timepoints not reasonable'})
            conf.save()

            activities_json_str = form.cleaned_data['activities']
            activities_json = json.loads(activities_json_str)
            
            try:
                
            except KeyError:
                pass                

            return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': 'invalid uploaded data'})

 def add_activity(conference, act_json):    
    form = ActivityInfoForm(request.POST)
    if form.is_valid():
        with database_transaction.atomic():
            try:
                conf = Conference.objects.get(pk=id) 
            except Conference.DoesNotExist:
                return JsonResponse({'message': 'conference does not exist'})

            org = utils.get_organization(request.user)
            assert org is not None
            if conf.organization.pk != org.pk:
                return JsonResponse({'message': 'permission error'})

            Activity.objects.create(
                conference=conf, start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'], place=form.cleaned_data['place'],
                activity=form.cleaned_data['activity'],
            )
            return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': 'invalid uploaded data'})

@user_has_permission('account.NormalUser_Permission')
def paper_submit(request, id):
    assert request.method == 'POST'
    with database_transaction.atomic():
        conf = Conference.objects.get(pk=id)
        normal_user = request.user.normaluser
        try:
            Submission.objects.create(
                submitter=normal_user, institute=request.POST['institute'],
                conference=conf, paper=request.FILES['paper'],
                paper_name=request.POST['paper_name'], 
                paper_abstract=request.POST['paper_abstract'],
                state='S', 
            )
            return JsonResponse({'message': 'success'})
        except MultiValueDictKeyError:
            return JsonResponse({'message': 'invalid uploaded data'})
