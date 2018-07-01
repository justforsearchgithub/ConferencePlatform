from django.test import TestCase, Client
from .models import *
from account.models import *
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission  

def add_permission(u, perm_str):
    content_type = ContentType.objects.get_for_model(User_Permission)
    permission = Permission.objects.get(content_type=content_type,
                                        codename=perm_str)
    u.user_permissions.add(permission)


def add_normal_user(email, password):
    u = User.objects.create_user(username=email, password=password, email=email)
    u.save()
    n = NormalUser.objects.create(
        user=u,
    )
    add_permission(u, 'NormalUser_Permission')
    u.save()

def add_org_user(email, password):
    u = User.objects.create_user(username=email, password=password, email=email)
    u.save()
    o = OrganizationUser.objects.create(
        user=u,
        org_name='BUAA',
        department='software',
        contacts='shiletong@buaa.edu.cn',
        phone_number='123123',
        address='xueyuanlu37',
    )
    add_permission(u, 'OrganizationUser_Permission')
    add_permission(u, 'ConferenceRelated_Permission')
    u.save()


class TestAddConference(TestCase):
    def setUp(self):
        add_normal_user('714465499@qq.com', '123456')
        add_org_user('shiletong@buaa.edu.cn', '123456')
        Subject.objects.create(name='renleixue')
    def test(self):
        c = Client()
        response = c.post('/account/login/', 
                    {'username':'shiletong@buaa.edu.cn', 'password':'123456'})
        self.assertEqual(response.status_code, 200)
        print(response.content)
        with open('/home/shiletong/fuckfuck') as fp:
            response = c.post('/conference/add_conference/', 
                    {'title':'chuibi dahui', 'subject': 'renleixue', 'template_no': 3,
                        'introduction': 'interesting', 'soliciting_requirement': 'meiyou',
                        'register_requirement': 'meiyou', 'accept_due': '2018-7-2 12:00',
                        'register_start': '2018-7-4 12:00', 'conference_start': '2018-7-5 12:00',
                        'conference_due': '2018-7-8 12:00', 'paper_template': fp,
                        'activities': 
                        '[{"start_time":"2018-7-6 12:00", "end_time":"2018-7-6 15:00", "place":"beijing", "activity":"chishi"}]'})
        #self.assertEqual(response.status_code, 200)
        print(response.content)
        print(Conference.objects.all()[0].pk)
        print(Conference.objects.all()[0].paper_template)
        """ for c in Conference.objects.all():
            print('Conference No.', c.pk)
            print('title: ', c.title)
            print('accept_due', c.accept_due)
            print('conference_due', c.conference_due)
            print('paper template content:')
            with open(c.paper_template, "r") as pt: """



