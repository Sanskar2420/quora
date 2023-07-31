import datetime

from celery import shared_task
from django.core.mail import send_mail

from quora import settings


@shared_task
def print_func(user):
    print(f"Hello this is time of current {datetime.datetime.now()}")
    send_email_to_user(user)
    return True


def send_email_to_user(user):
    subject = 'Testing of Email Sending using Celery in Quora Application'
    message = f'Hi {user}, Thank you for choosing celery to perform email sending task'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user, ]
    print(recipient_list, '--------------------------------------------->')
    send_mail(subject, message, email_from, recipient_list)
    print("here Email is shared successfully.")
