from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('change_password/', views.change_password, name='change_password'),
    path('normal_user_register/', views.normal_user_register, name='normal_user_register')
    path('organization_user_register/', views.organization_user_register, name='organization_user_register'),
    path('organization_sub_user_register/', views.organization_sub_user_register, name='organization_sub_user_register'),
    
    
]