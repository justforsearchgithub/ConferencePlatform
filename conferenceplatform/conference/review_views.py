from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse
from .utils import *
from account.models import *
from account.decorators import user_has_permission
from django.db import transaction as database_transaction
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError
from django import forms
from account.tasks import my_send_email
from django.core.mail import send_mail
from conferenceplatform.settings import DEFAULT_FROM_EMAIL

@user_has_permission('account.ConferenceRelated_Permission')
def review_submission(request,id):
    assert request.method == 'POST'    
    cleaner = forms.CharField()
    try:
        with database_transaction.atomic():
            sub = Submission.objects.get(pk=id)
            conf = sub.conference
            org_login = get_organization(request.user)
            if org_login == None or org_login.pk != conf.organization.pk:
                return JsonResponse({'message': 'permission error'})
            conf_status = conference_status(conf)
            
            state = cleaner.clean(request.POST['state_choice'])
            sub.state = state
            con_name = sub.conference.title
            if state == 'P':
                subject = 'congratulations'
                message = 'your submission in ' + con_name + ' has been passed'
            elif state == 'R':
                subject = 'sorry'
                message = 'your submission in ' + con_name + ' has been rejected'
            elif state == 'M':
                if conf_status != ConferenceStatus.reviewing_accepting_modification:
                    return JsonResponse({'message': 'not in modification period'})
                advice = cleaner.clean(request.POST['advice'])
                sub.modification_advice = advice
                subject = 'information'
                message = 'your submission in ' + con_name + ' should be modified.\nModified advice: ' + advice
            else:
                return JsonResponse({'message': 'invalid state choice'})
            sub.save()
            my_send_email(subject, message, [].append(sub.submitter.user.username))
            return JsonResponse({'message': 'success'})
    except Submission.DoesNotExist:
        return JsonResponse({'message': 'invalid submission pk'})
    except MultiValueDictKeyError:
        return JsonResponse({'message': 'invalid uploaded data'})
    except ValidationError:
        return JsonResponse({'message': 'invalid uploaded data'})