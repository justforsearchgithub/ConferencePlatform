from django.urls import path
from . import display_views

app_name = 'account'
urlpatterns = [
    path('my_conference/', display_views.get_conferences_by_organization, name='my_conferences'),
    path('my_submission/', display_views.get_submissions_by_submitter, name='my_submission'),
    path('test',display_views.test1,name='test')
]