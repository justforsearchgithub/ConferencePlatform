from account.tasks import my_send_email
from celery import task
from conference.models import *
from account.models import *
from datetime import datetime, timedelta
from .email import *


@task
def send_register_start_email():
    today = datetime.now()
    day = datetime.now() + timedelta(days=1)
    conferences = Conference.objects.filter(register_start__range=(today, day))
    for conference in conferences:
        collect_users = conference.collect_user.all()
        for user in collect_users:
            my_send_email(SUBJECT['register_start'],
                          MESSAGE['register_start'].format(user.user.username, conference.title, conference.register_due),
                          user.user.username)
    return True


@task
def send_register_due_email():
    today = datetime.now()
    day = datetime.now() + timedelta(days=1)
    conferences = Conference.objects.filter(register_due__range=(today, day))
    for conference in conferences:
        collect_users = conference.collect_user.all()
        for user in collect_users:
            my_send_email(SUBJECT['register_due'],
                          MESSAGE['register_due'].format(user.user.username, conference.title, conference.register_due),
                          user.user.username)
    return True


@task
def send_accept_due_email():
    today = datetime.now()
    day = datetime.now() + timedelta(days=1)
    conferences = Conference.objects.filter(accept_due__range=(today, day))
    for conference in conferences:
        collect_users = conference.collect_user.all()
        for user in collect_users:
            my_send_email(SUBJECT['accept_due'],
                          MESSAGE['accept_due'].format(user.user.username, conference.title, conference.accept_due),
                          user.user.username)
    return True


@task
def send_modify_due_email():
    today = datetime.now()
    day = datetime.now() + timedelta(days=1)
    conferences = Conference.objects.filter(modify_due__range=(today, day))
    for conference in conferences:
        submissions = conference.submission_set.filter(state='M')
        for submission in submissions:
            my_send_email(SUBJECT['modify_due'],
                          MESSAGE['modify_due'].format(submission.submitter.user.username, conference.title, conference.modify_due),
                          submission.submitter.user.username)
    return True