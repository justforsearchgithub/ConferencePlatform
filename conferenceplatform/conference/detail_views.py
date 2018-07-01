from django.shortcuts import render
from django.http import JsonResponse
from .utils import *
from account.decorators import user_has_permission


@user_has_permission('account.OrganizationUser_Permission')
def conference_information(request, id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        conference = Conference.objects.get(pk=id)
        data = {
            'organization': conference.organization,
            'title': conference.title,
            'subject': conference.subject,
            'introduction': conference.introduction,
            'soliciting_requirement': conference.soliciting_requirement,
            'paper_template': conference.paper_template,
            'register_requirement': conference.register_requirement,
            'accept_start': conference.accept_start,
            'accept_due': conference.accept_due,
            'modify_due': conference.modify_due,
            'register_start': conference.register_start,
            'conference_start': conference.conference_start,
            'conference_due': conference.conference_due,
        }
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except Conference.DoesNotExist:
        result['message'] = ['invalid conference pk']
        return JsonResponse(result)


def subject_information(request):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        subjects = Subject.objects.all()
        data = {'names': []}
        for i in subjects:
            data['names'].append(i.name)
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except Subject.DoesNotExist:
        result['message'] = ['invalid subject pk']
        return JsonResponse(result)


def activity_information(request,id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        activity = Activity.objects.get(pk=id)
        data = {
            'conference': activity.conference.pk,
            'start_time': activity.start_time,
            'end_time': activity.end_time,
            'place': activity.place,
            'activity': activity.activity,
        }
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except Activity.DoesNotExist:
        result['message'] = ['invalid activity pk']
        return JsonResponse(result)


def submission_information(request,id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        submission = Submission.objects.get(pk=id)
        data = {
            'submitter': submission.submitter.pk,
            'conference': submission.conference.pk,
            'paper': submission.paper,
            'paper_name': submission.paper_name,
            'paper_abstract': submission.paper_abstract,
            'authors': submission.authors,
            'institute': submission.institute,
            'submit_time': submission.submit_time,
            'modification_advice': submission.modification_advice,
            'modified': submission.modified,
            'modified_time': submission.modified_time,
            'modified_explain': submission.modified_explain,
            'state': submission.state,
        }
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except Submission.DoesNotExist:
        result['message'] = ['invalid submission pk']
        return JsonResponse(result)


def register_information(request, id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        info = RegisterInformation.objects.get(pk=id)
        data = {
            'user': info.user.pk,
            'conference': info.conference.pk,
            'submission': info.sumbission.pk,
            'participants': info.participants,
            'pay_voucher': info.pay_voucher,
        }
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except RegisterInformation.DoesNotExist:
        result['message'] = ['invalid register information pk']
        return JsonResponse(result)