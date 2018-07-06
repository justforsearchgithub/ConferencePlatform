from account.tasks import my_send_email
from celery import task
from conference.models import *
from account.models import *
from datetime import datetime, timedelta

@task
def send_register_email():
    day = datetime.now() + timedelta(days=1)
    conferences = Conference.objects.filter()
    return 1