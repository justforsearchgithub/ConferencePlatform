from django.urls import path
from . import views, detail_views

app_name = 'conference'
urlpatterns = [
    path('add_conference/', views.add_conference, name='add_conference'),
    path('conference/<int:id>/paper_submit/', views.paper_submit, name='paper_submit'),
    path('conference/<int:id>/register/', views.conference_register, name='conference_register'),
    path('conference/<int:id>/information/', detail_views.conference_information, name='conference_information'),
    path('subjects/', detail_views.subject_information, name='subject_information'),
    path('activity/<int:id>/', detail_views.activity_information, name='activity_information'),
    path('submission/<int:id>/', detail_views.submission_information, name='submission_information'),
    path('register_information/<int:id>/', detail_views.register_information, name='register_information'),
]