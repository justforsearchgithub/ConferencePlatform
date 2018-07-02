from django.shortcuts import render
from django.http import JsonResponse
from account.decorators import user_has_permission
from conference.models import *
from .models import *
from conference import detail_views
from account import decorators


@user_has_permission('account.ConferenceRelated_Permission')
def get_conferences_by_organization(request):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        if request.user.has_perm('account.OrganizationSubUser_Permission'):
            org_sub_user = OrganizationSubUser.objects.get(user=request.user)
            organization = org_sub_user.organization
        elif request.user.has_perm('account.OrganizationUser_Permission'):
            organization = OrganizationUser.objects.get(user=request.user)
        else:
            return JsonResponse({'message': 'permission error'})
        conferences = Conference.objects.filter(organization=organization)
        data = []
        for con in conferences:
            data.append({
                'conference_id': con.pk,
                'conference_title': con.title,
            })
        result['data'] = data
        result['message'] = 'success'
    except Conference.DoesNotExist:
        result['message'] = ['no conference']
    except OrganizationUser.DoesNotExist:
        result['message'] = ['invalid organization user']
    except OrganizationSubUser.DoesNotExist:
        result['message'] = ['invalid organization sub user']
    return JsonResponse(result)


@user_has_permission('account.NormalUser_Permission')
def get_submissions_by_submitter(request):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        submissions = Submission.objects.filter(submitter=request.user)
        data = []
        for sub in submissions:
            data.append({
                'submission_id': sub.pk,
                'paper_name': sub.paper_name,
            })
        result['data'] = data
        result['message'] = 'success'
    except Submission.DoesNotExist:
        result['message'] = ['no submissions']
    return JsonResponse(result)


def test1(request):
    return JsonResponse({'123': '123'})


@user_has_permission('account.ConferenceRelated_Permission')
def get_papers_by_conference(request, id):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        conference = Conference.objects.get(pk=id)
        if conference.organization.user != request.user:
            return JsonResponse({'message': 'permission error'})
        papers = Submission.objects.filter(conference=conference)
        data = []
        for paper in papers:
            data.append({
                'submission_id': paper.pk,
                'paper_name': paper.paper_name,
            })
        result['data'] = data
        result['message'] = 'success'
    except Submission.DoesNotExist:
        result['message'] = ['no submissions']
    except Conference.DoesNotExist:
        result['message'] = ['no conference']
    return JsonResponse(result)


def get_activities_by_conference(request, id):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        conference = Conference.objects.get(pk=id)
        activities = Activity.objects.filter(conference=conference)
        data = []
        for activity in activities:
            data.append({
                'activity_id': activity.pk,
                'activity_name': activity.activity,
                'start_time': activity.start_time,
                'end_time': activity.end_time,
                'place': activity.place,
            })
        result['data'] = data
        result['message'] = 'success'
    except Activity.DoesNotExist:
        result['message'] = ['no activities']
    except Conference.DoesNotExist:
        result['message'] = ['no conference']
    return JsonResponse(result)