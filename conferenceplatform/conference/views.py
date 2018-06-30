from django.shortcuts import render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db import transaction as database_transaction   
import datetime

from account.models import *
from .models import *
from .forms import *
import utils



def add_conference(request):
    assert request.method == 'POST'
    form = ConferenceInfoForm(request.POST, request.FILES)

    if form.is_valid():
        with database_transaction.atomic():
            org = utils.get_organization(request.user)
            if org is None:
                return JsonResponse({'message': 'permission denied'})
            Conference.objects.create(
                origanization=org, title=form.cleaned_data['title'], 
                subject=form.cleaned_data['subject'],
                introduction=form.cleaned_data['introduction'], 
                soliciting_requirement=form.cleaned_data['soliciting_requirement'],            
                register_requirement=form.cleaned_data['register_requirement'],
                accept_start=form.cleaned_data['accept_start'],
                accept_due=form.cleaned_data['accept_due'],
                # modify_due=form.cleaned_data['modify_due'],
                register_start=form.cleaned_data['register_start'],
                conference_start=form.cleaned_data['conference_start'],
                conference_due=datetime.cleaned_data['conference_due']

                paper_template=form.paper_template
            )
            return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': 'invalid uploaded data'})
    
 def add_activity(request, id):
    assert request.method == 'POST'
    
    form = ActivityInfoForm(request.POST)
    if form.is_valid():
        with database_transaction.atomic():
            try:
                conf = Conference.objects.get(pk=id) 
            except Conference.DoesNotExist:
                return JsonResponse({'message': 'conference does not exist'})

            org = utils.get_organization(request.user)
            if org is None or conf.organization.pk != org.pk:
                return JsonResponse({'message': 'permission denied'})

            Activity.objects.create(
                conference=conf, start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'], place=form.cleaned_data['place'],
                activity=form.cleaned_data['activity'],
            )
            return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': 'invalid uploaded data'})

def paper_submit(request)