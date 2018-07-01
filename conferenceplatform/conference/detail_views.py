from django.shortcuts import render
from django.http import JsonResponse
from .utils import *
from account.models import *
from account.decorators import user_has_permission


def get_conference_detail(conference):
    data = {
        'organization': get_organization_detail(conference.organization),
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
    return data

def get_organization_detail(org):
    data = {
        'org_id': org.pk,
        'org_name': org.org_name,
        'department': org.department,
        'contacts': org.contacts,
        'phone_number': org.phone_number,
        'address': org.address,
    }
    return data

def get_activity_detail(activity):
    data = {
        'conference_id': activity.conference.pk,
        'conference_title': activity.conference.title,
        'start_time': activity.start_time,
        'end_time': activity.end_time,
        'place': activity.place,
        'activity': activity.activity,
    }
    return data

def get_submission_detail(submission):
    data = {
        'submitter_id': submission.submitter.pk,
        'conference_id': submission.conference.pk,
        'conference_title': submission.conference.title,
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
    return data

def get_register_detail(info):
    data = {
        'user_id': info.user.pk,
        'conference_id': info.conference.pk,
        'submission_id': info.sumbission.pk,
        'participants': info.participants,
        'pay_voucher': info.pay_voucher,
    }
    return data


#@user_has_permission('account.OrganizationUser_Permission')
def conference_information(request, id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        conference = Conference.objects.get(pk=id)
        data = get_conference_detail(conference)
        data['organization'] = conference.organization
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
        result['message'] = ['no subjects']
        return JsonResponse(result)


def activity_information(request,id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        activity = Activity.objects.get(pk=id)
        data = get_activity_detail(activity)
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
        data = get_submission_detail(submission)
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
        data = get_register_detail(info)
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except RegisterInformation.DoesNotExist:
        result['message'] = ['invalid register information pk']
        return JsonResponse(result)
