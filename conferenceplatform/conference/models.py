from django.db import models
from account.models import EnterpriseUser

class Conference(models.Model):
    enterprise = models.ForeignKey(EnterpriseUser, on_delete=models.CASCADE)
    title = models.CharField(200)
    