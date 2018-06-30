from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('add_conference/', views.add_conference, name='add_conference'),
    path('conference/<int:id>/add_activity/', views.add_activity, name='add_activity'),
    path('conference/<int:id>/paper_submit/', views.paper_submit, name='paper_submit'),
    path('conference/<int:id>/register/', views.conference_register, name='conference_register'),
]