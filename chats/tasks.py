import datetime

from celery import shared_task
from django.core.mail import send_mail

from quora import settings


@shared_task
def print_func(sender_name, receiver_name, receiver_email):
    print(f"Hello this is the current time : {datetime.datetime.now()}")
    send_notification_email_to_user(sender_name=sender_name, receiver_name=receiver_name, receiver_email=receiver_email)
    return True


def send_notification_email_to_user(sender_name, receiver_name, receiver_email):
    subject = f'Chat message notification from the {sender_name}'
    message = f'Hi {receiver_name}, This is an notification email to make you aware that there are some new messages'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [receiver_email, ]
    print(recipient_list, '--------------------------------------------->')
    send_mail(subject, message, email_from, recipient_list)
    print("here Email is shared successfully.")
