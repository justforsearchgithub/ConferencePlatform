from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NormalUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)


class EnterpriseUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class EnterpriseSubUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(EnterpriseUser, on_delete=models.CASCADE)


class OurAdmin(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)



class User_Permission(models.Model):
    class Meta:
        permissions = (
            ('NormalUser_Permission', 'permission for Normal User'),
            ('EnterpriseUser_Permission', 'permission for Enterprise User'),
            ('EnterpriseSubUser_Permission',  'permission for Enterprise Sub User'),
            ('OurAdmin_Permssion', 'permission for Admin'),
        )
