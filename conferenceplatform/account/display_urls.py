from django.urls import path
from . import display_views

urlpatterns = [
    path('my_conference/', display_views.get_conferences_by_organization, name='my_conferences'),
    path('my_submission/', display_views.get_submissions_by_submitter, name='my_submission'),
    path('conference/<int:id>/papers/', display_views.get_papers_by_conference, name='conference_papers'),
    path('test/', display_views.test1, name='test')
]