from django.db.models.signals import post_save
from django.dispatch import receiver
from chats.tasks import print_func

from chats.models import Messages


@receiver(post_save, sender=Messages)
def handler_func(sender, **kwargs):
    print(kwargs)
    message = kwargs.get('instance')
    if message:
        # need to implement logic of email notification using celery.
        print_func.delay(sender_name=message.sender.username, receiver_name=message.receiver.username,
                         receiver_email=message.receiver.email)
        pass
    print("---------------------------------> Hello #THis is called when you send any message: Thank you so much")
