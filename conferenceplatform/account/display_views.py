from django.shortcuts import render
from django.http import JsonResponse
from account.decorators import user_has_permission
from conference.models import *
from .models import *
from conference import detail_views


def get_conferences_by_organization(request):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        organization = OrganizationUser.objects.get(user=request.user)
        if organization is None:
            orgSubUser = OrganizationSubUser.objects.get(user=request.user)
            organization = orgSubUser.organization
        conferences = Conference.objects.filter(organization=organization)
        data = []
        for con in conferences:
            #data.append(detail_views.get_conference_detail(con))
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


def get_submissions_by_submitter(request):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        submissions = Submission.objects.get(submitter=request.user)
        data = []
        for sub in submissions:
            #data.append(detail_views.get_submission_detail(sub))
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


def get_papers_by_conference(request, id):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        conference = Conference.objects.get(pk=id)
        papers = Submission.objects.get(conference=conference)
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
