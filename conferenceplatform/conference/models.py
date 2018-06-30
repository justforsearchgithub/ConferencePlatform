from django.db import models
from account.models import OrganizationUser, NormalUser

def conference_directory_path(instance, filename):
    return 'conference_{0}/{1}'.format(instance.conference.pk, filename)


class Subject(models.Model):
    name = models.CharField(max_length=200,primary_key=True)

class Conference(models.Model):
    organization = models.ForeignKey(OrganizationUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    introduction = models.TextField()
    soliciting_requirement = models.TextField()
    paper_template = models.FileField(upload_to=conference_directory_path)
    register_requirement = models.TextField()

    accept_start = models.DateTimeField(auto_now=True)
    accept_due = models.DateTimeField(blank=True, null=True)
    modify_due = models.DateTimeField(blank=True, null=True)
    # 中间有一个审核状态
    register_start = models.DateTimeField(blank=True, null=True)
    conference_start = models.DateTimeField()
    conference_due = models.DateTimeField()

class Activity(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)

class Submission(models.Model):
    submitter = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    paper = models.FileField(upload_to=conference_directory_path)
    paper_name = models.CharField(max_length=200)
    paper_abstract = models.TextField()
    authors = models.CharField(max_length=255)
    institute = models.CharField(max_length=200)
    
    submit_time = models.DateTimeField(auto_now=True)

    modification_advice = models.TextField(null=True)
    modified = models.BooleanField(default=False)
    modified_time = models.DateTimeField(blank=True, null=True)
    modified_explain = models.TextField(blank=True, null=True)    

    STATE_CHOICES = (
        ('S', 'Suspending'),
        ('P', 'Passed'),
        ('M', 'NeedModify'),
        ('R', 'Rejected'),
    )
    state = models.CharField(max_length=1, choices=STATE_CHOICES)

    class meta:
        unique_together = ('submitter', 'conference')

    


class RegisterInformation(models.Model):
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    participants = models.TextField()
    pay_voucher = models.FileField(upload_to=conference_directory_path)

    class meta:
        unique_together=('user', 'conference')