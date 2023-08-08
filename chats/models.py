from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import SET, Q
from users.models import User


class Room(models.Model):
    sender = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='sender')
    receiver = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='receiver')
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_room_by_sender_receiver(cls, kwargs):
        return cls.objects.filter(
            Q(sender=kwargs.get('sender'), receiver=kwargs.get('receiver')) | Q(sender=kwargs.get('receiver'),
                                                                                receiver=kwargs.get('sender')))

    @classmethod
    def get_room(cls, kwargs):
        return cls.objects.filter(**kwargs)

    @classmethod
    def create_room(cls, kwargs):
        return cls.objects.create(**kwargs)


class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='message_sender')
    receiver = models.ForeignKey(User, on_delete=SET(AnonymousUser.id), related_name='message_receiver')
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_message(cls, kwargs):
        message_Data = {
            'sender': User.get_user(filter_kwargs={"id": kwargs.get("sender")}),
            'receiver': User.get_user(filter_kwargs={"id": kwargs.get("receiver")}),
            'message': kwargs.get('message')}
        # return message
        return cls.objects.create(**message_Data)

    @classmethod
    def get_all_messages(cls, kwargs):
        return cls.objects.filter(
            Q(sender_id=kwargs.get('sender'), receiver_id=kwargs.get('receiver')) | Q(sender_id=kwargs.get('receiver'),
                                                                                      receiver_id=kwargs.get(
                                                                                          'sender'))).order_by('time')
