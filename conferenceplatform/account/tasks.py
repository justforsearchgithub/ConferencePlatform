from django.core.mail import send_mail
from celery import task

@task
def send_register_email(email):
    subject = '测试注册信息'
    message = '测试注册成功'
    to_email = list()
    to_email.append(email)
    send_mail(
        subject,
        message,
        'demonsNearby@163.com',
        to_email,
        fail_silently=False
    )


@task
def my_send_email(subject, message, to_email):
    send_mail(
        subject,
        message,
        'demonsNearby@163.com',
        to_email,
        fail_silently=False
    )
    