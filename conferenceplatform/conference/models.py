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
    soliciting_request = models.TextField()
    paper_template = models.FileField(upload_to=conference_directory_path)
    register_request = models.TextField()

    start_accept_time = models.DateTimeField(auto_now=True)
    stop_accept_time = models.DateTimeField(blank=True, null=True)
    stop_modify_time = models.DateTimeField(blank=True, null=True)
    # 中间有一个审核状态
    regiser_start_time = models.DateTimeField(blank=True, null=True)
    conference_start_time = models.DateTimeField()
    conference_end_time = models.DateTimeField()

class Activity(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)

class Submission(models.Model):
    submitter = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    institute = models.CharField(max_length=200)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    modified = models.BooleanField(default=False)
    submit_time = models.DateTimeField(auto_now=True)
    modified_time = models.DateTimeField(blank=True, null=True)
    paper = models.FileField(upload_to=conference_directory_path)
    paper_name = models.CharField(max_length=200)
    paper_abstract = models.TextField()
    modified_message = models.CharField(blank=True, null=True)

    STATE_CHOICES = (
        ('P', 'Passed'),
        ('M', 'NeedModify'),
        ('R', 'Rejected'),
    )
    state = models.CharField(max_length=1, choices=STATE_CHOICES)
    modify_request = models.TextField(null=True)


class RegisterInformation(models.Model):
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    people = models.TextField()
    pay_voucher = models.FileField(upload_to=conference_directory_path)
    description = models.TextField()

    class meta:
        unique_together=('user', 'conference')