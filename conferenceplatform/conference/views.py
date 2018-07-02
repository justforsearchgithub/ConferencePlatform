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
    if form.is_valid() or True:
        with database_transaction.atomic():
            org = get_organization(request.user)
            assert org is not None
            try:
                subject = Subject.objects.get(name=form.cleaned_data['subject'])
            except Subject.DoesNotExist:
                print('BUG: no subject: ' + form.cleaned_data['subject'])

            conf = Conference.objects.create(
                organization=org, title=form.cleaned_data['title'], 
                subject=subject,
                template_no=form.cleaned_data['template_no'],
                introduction=form.cleaned_data['introduction'], 
                soliciting_requirement=form.cleaned_data['soliciting_requirement'],            
                register_requirement=form.cleaned_data['register_requirement'],
                accept_start=datetime.datetime.now(),
                accept_due=form.cleaned_data['accept_due'],
                # modify_due=form.cleaned_data['modify_due'],
                register_start=form.cleaned_data['register_start'],
                register_due=form.cleaned_data['register_due'],
                conference_start=form.cleaned_data['conference_start'],
                conference_due=form.cleaned_data['conference_due'],
                #paper_template=form.cleaned_data['paper_template'],
            )
            conf.paper_template = request.FILES['paper_template']
            conf.save()
            if not valid_timepoints(conf):
                conf.delete()
                return JsonResponse({'message': 'timepoints not reasonable'})            

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
            if conference_status(conf) != ConferenceStatus.accepting_submission:
                return JsonResponse({'message': 'wrong time range'})
            normal_user = request.user.normaluser
            s = Submission.objects.create(
                submitter=normal_user, institute=request.POST['institute'],
                conference=conf, 
                #paper=request.FILES['paper'],
                paper_name=request.POST['paper_name'], 
                paper_abstract=request.POST['paper_abstract'],
                authors=request.POST['authors'],
                state='S', 
            )
            s.paper = request.FILES['paper']
            s.save()
            conf.num_submission = conf.num_submission + 1
            conf.save()
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
            if conference_status(conf) != ConferenceStatus.accepting_register:
                return JsonResponse({'message': 'wrong time range'})
            if request.POST['listen_only'] == 'false':
                paper_submission_id = int(request.POST['paper_id'])            
                paper_submission = Submission.objects.get(pk=paper_submission_id)
                if (paper_submission.submitter.pk != request.user.normaluser.pk 
                   or paper_submission.conference.pk != conf.pk):
                    return JsonResponse({'message': 'not matching'})
                if paper_submission.state != 'P':
                    return JsonResponse({'message': 'paper not passed'})
                r = RegisterInformation.objects.create(
                    user=request.user.normaluser,
                    conference=conf,
                    participants=request.POST['participants'],
                    submission=paper_submission,
                    # pay_voucher=request.FILES['pay_voucher'],
                )
            else:
                assert request.POST['listen_only'] == 'true'
                # listen only
                r = RegisterInformation.objects.create(
                    user=request.user.normaluser,
                    conference=conf,
                    participants=request.POST['participants'],
                )
            r.pay_voucher = request.FILES['pay_voucher']
            r.save()
            return JsonResponse({'message': 'success'})
    except Conference.DoesNotExist:
        return JsonResponse({'message': 'invalid conference pk'})
    except MultiValueDictKeyError:
        return JsonResponse({'message': 'invalid uploaded data'})
    except IntegrityError:
        return JsonResponse({'message': 'reduplicate register'})
    except Submission.DoesNotExist:
        return JsonResponse({'message': 'invalid paper id'})


@user_has_permission('account.ConferenceRelated_Permission')
def set_modify_due(request, id):
    assert request.method == 'POST'
    now = datetime.datetime.now()
    try:
        with database_transaction.atomic():
            conf = Conference.objects.get(pk=id)
            if conf.modify_due != None:
                return JsonResponse({'message': 'already set'})

            cleaner = forms.DateTimeField()
            due = cleaner.clean(request.POST['modify_due'])
            if due <= now:
                return JsonResponse({'message': 'too late'})
            
            conf.modify_due = due
            if not valid_timepoints(conf):
                conf.modify_due = None
                retrn JsonResponse({'message': 'time point'})
            
    except Conference.DoesNotExist:
        return JsonResponse({'message': 'invalid conference pk'})
    except MultiValueDictKeyError:
        return JsonResponse({'message': 'invalid uploaded data'})