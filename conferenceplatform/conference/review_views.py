from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse
from .utils import *
from account.models import *
from account.decorators import user_has_permission
from django.db import transaction as database_transaction
from django.utils.datastructures import MultiValueDictKeyError
from django import forms
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
            if (conf_status != ConferenceStatus.reviewing_accepting_modification
                and conf_status != ConferenceStatus.reviewing):
                return JsonResponse({'message': 'not reviewing'})
            
            state = cleaner.clean(request.POST['state_choice'])
            if state == 'P':
                sub.state = state
                con_name = sub.conference.title
                """ send_mail(subject='congratulations', message='your submission in '+con_name+' has been passed',
                          from_email=DEFAULT_FROM_EMAIL, ail_silently=False)                 """
            elif state == 'R':
                sub.state = state                
                #send email                
            elif state == 'M':
                if conf_status != ConferenceStatus.reviewing_accepting_modification:
                    return JsonResponse({'message': 'not in modification period'})
                sub.state = state
                sub.modification_advice = cleaner.clean(request.POST['advice'])
                # send mail                
            else:
                return JsonResponse({'message': 'invalid state choice'})
            sub.save()
            return JsonResponse({'message': 'success'})
    except Submission.DoesNotExist:
        return JsonResponse({'message': 'invalid submission pk'})
    except MultiValueDictKeyError:
        return JsonResponse({'message': 'invalid uploaded data'})
    except ValidationError:
        print('invalid2')
        return JsonResponse({'message': 'invalid uploaded data'})