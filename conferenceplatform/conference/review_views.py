from django.shortcuts import render
from django.http import JsonResponse
from .utils import *
from account.models import *
from account.decorators import user_has_permission
from django.db import transaction as database_transaction
from django.core.mail import send_mail
from conferenceplatform.settings import DEFAULT_FROM_EMAIL

def review_submission(request,id):
    assert request.method == 'POST'
    try:
        with database_transaction.atomic():
            sub = Submission.objects.get(pk=id)
            state = request.POST['state_choice']
            if state == 'P':
                sub.state = state
                con_name = sub.conference.title
                send_mail(subject='congratulations', message='your submission in '+con_name+' has been passed',
                          from_email=DEFAULT_FROM_EMAIL, ail_silently=False)
                return JsonResponse({'message': 'success'})
            elif state == 'R':
                sub.state = state
                #send email
                return JsonResponse({'message': 'success'})
            else:
                return JsonResponse({'message': 'invalid state choice'})
    except Submission.DoesNotExist:
        return JsonResponse({'message': 'invalid state choice'})