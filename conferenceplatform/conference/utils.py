from django.utils import timezone
from enum import Enum
from .models import *
import datetime

class ConferenceStatus(Enum):
    not_started = 1
    accepting_submission = 2
    accepting_modification = 3
    reviewing = 4 # 结束接受修改后和开始会议注册前
    accepting_register = 5
    meeting = 6
    over = 7 # 


def get_organization(user):
    if user.has_perm('account.OrganizationUser_Permission'):
        return user.organizationuser
    elif user.has_perm('account.OrganizationSubUser_Permission'):
        return user.organizationsubuser.organization
    else:
        return None

def valid_timepoints(conf):
    res =  (conf.accept_start < conf.accept_due 
        and conf.register_start < conf.conference_start
        and conf.conference_start < conf.conference_due)
    if conf.modify_due != None:
        res = (res and conf.accept_due < conf.modify_due 
                and conf.modify_due < conf.register_start)
    return res

def conference_status(conf):
    now = datetime.datetime.now()
    if now < conf.accept_start:
        return ConferenceStatus.not_started
    elif now < conf.accept_due:
        return ConferenceStatus.accepting_submission
    elif now < conf.modify_due:
        return ConferenceStatus.accepting_modification
    elif now < conf.register_start:
        return ConferenceStatus.reviewing
    elif now < conf.conference_start:
        return ConferenceStatus.accepting_register
    elif now < conf.conference_due:
        return ConferenceStatus.meeting
    else:
        return ConferenceStatus.over

def add_activity(conference, act_json):    
     Activity.objects.create(
         conference=conference,
         start_time=act_json['start_time'],
         end_time=act_json['end_time'],
         place=act_json['place'],
         activity=act_json['activity'],
     )
