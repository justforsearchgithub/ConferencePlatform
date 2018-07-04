from django.urls import path
from . import views, detail_views, edit_views

app_name = 'conference'
urlpatterns = [
    path('add_conference/', views.add_conference, name='add_conference'),
    path('conference/<int:id>/paper_submit/', views.paper_submit, name='paper_submit'),
    path('conference/<int:id>/register/', views.conference_register, name='conference_register'),
    path('conference/<int:id>/information/', detail_views.conference_information, name='conference_information'),
    path('conference/<int:id>/set_modify_due/', views.set_modify_due, name='set_modify_due'),
    path('subjects/', detail_views.subject_information, name='subject_information'),
    path('activity/<int:id>/', detail_views.activity_information, name='activity_information'),
    path('submission/<int:id>/', detail_views.submission_information, name='submission_information'),
    path('register_information/<int:id>/', detail_views.register_information, name='register_information'),
    path('top10_hot_references/', detail_views.top10_hot_conferences, name='top10_hot_references'),
    path('num_not_over/', views.num_not_over, name='num_not_over'),

    path('edit_conference/<int:id>/', edit_views.edit_conference_by_id, name='edit_conference'),
    path('edit_activity/<int:id>/', edit_views.edit_activity_by_id, name='edit_activity'),
]