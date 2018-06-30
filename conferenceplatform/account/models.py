from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NormalUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

def organization_directory_path(instance, filename):
    return 'organization_{0}/{1}'.format(instance.pk, filename)


class OrganizationUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    contacts = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    bussiness_license = models.FileField()
    id_card_front = models.FileField(upload_to=organization_directory_path)
    id_card_reverse = models.FileField(upload_to=organization_directory_path)
    

class OrganizationSubUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(OrganizationUser, on_delete=models.CASCADE)


class OurAdmin(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)


class User_Permission(models.Model):
    class Meta:
        permissions = (
            ('NormalUser_Permission', 'permission for Normal User'),
            ('OrganizationUser_Permission', 'permission for Organization User'),
            ('OrganizationSubUser_Permission',  'permission for Organization Sub User'),
            ('OurAdmin_Permssion', 'permission for Admin'),
            ('ConferenceRelated_Permission', 'permission for Conference Related actions')
        )
