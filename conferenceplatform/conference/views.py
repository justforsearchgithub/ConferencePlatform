from django.shortcuts import render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db import transaction as database_transaction   
from django.db import IntegrityError, DatabaseError
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
            org = get_organization(request.user)
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
            if not valid_timepoints(conf):
                return JsonResponse({'message': 'timepoints not reasonable'})
            conf.save()

            activities_json_str = form.cleaned_data['activities']
            activities_json = json.loads(activities_json_str)
            
            try:
                for activity in activities_json:
                    add_activity(conf, activity)
            except KeyError as e:
                print(e)
            return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': 'invalid uploaded data'})


@user_has_permission('account.NormalUser_Permission')
def paper_submit(request, id):
    assert request.method == 'POST'
    try:
        with database_transaction.atomic():
            conf = Conference.objects.get(pk=id)
            normal_user = request.user.normaluser
            Submission.objects.create(
                submitter=normal_user, institute=request.POST['institute'],
                conference=conf, paper=request.FILES['paper'],
                paper_name=request.POST['paper_name'], 
                paper_abstract=request.POST['paper_abstract'],
                authors=request.POST['authors'],
                state='S', 
            )
            return JsonResponse({'message': 'success'})
    except Conference.DoesNotExist:
        return JsonResponse({'message': 'invalid conference pk'})
    except MultiValueDictKeyError:
        return JsonResponse({'message': 'invalid uploaded data'})
    except IntegrityError:
        return JsonResponse({'message': 'multiple submission'})

@user_has_permission('account.NormalUser_Permission')
def conference_register(request, id):
    assert request.method == 'POST'
    try:
        with database_transaction.atomic():
            conf = Conference.objects.get(pk=id)
            paper_submission_id = int(request.POST['paper_id'])            
            paper_submission = Submission.objects.get(pk=paper_submission_id)
            if paper_submission.submitter.pk != request.user.normaluer.pk \
                or paper_submission.conference.pk != conf.pk:
                return JsonResponse({'message': 'not matching'})
            RegisterInfomation.objects.create(
                user=request.user.normaluser,
                conference=conf,
                participants=request.POST['participants'],
                submission=paper_submission,
                pay_voucher=request.FILES['pay_voucher'],
            )
            return JsonResponse({'message': 'success'})
    except Conference.DoesNotExist:
        return JsonResponse({'message': 'invalid conference pk'})
    except MultiValueDictKeyError:
        return JsonResponse({'message': 'invalid uploaded data'})
    except IntegrityError:
        return JsonResponse({'message': 'reduplicate register'})
    except Submission.DoesNotExist:
        return JsonResponse({'message': 'invalid paper id'})

