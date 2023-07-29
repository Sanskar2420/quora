from django.contrib.auth.models import AbstractUser
from django.db import models

status_choice = [('ACCEPTED', 'ACCEPTED'), ('PENDING', 'PENDING'), ('REJECTED', 'REJECTED')]


class User(AbstractUser):
    @classmethod
    def create_user(cls, kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def update_user(cls, filter_kwargs, update_kwargs):
        return cls.objects.filter(**filter_kwargs).update(**update_kwargs)

    @classmethod
    def get_user(cls, filter_kwargs=None):
        return cls.objects.filter(**filter_kwargs).first() if filter_kwargs else cls.objects.filter()

    @classmethod
    def get_user_exclude(cls, filter_kwargs=None, exclude_filter=None):
        if not filter_kwargs:
            filter_kwargs = {}
        if not exclude_filter:
            exclude_filter = {}
        return cls.objects.filter(**filter_kwargs).exclude(**exclude_filter)

    @classmethod
    def set_new_password(cls, user, password):
        """
        set user password
        @param user: user
        @param password: user password
        """
        user.set_password(password)
        user.save()

    # Create your models here.


class FollowTable(models.Model):
    request_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_by')
    request_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_to')
    status = models.CharField(choices=status_choice, default='PENDING', max_length=15)

    @classmethod
    def get_users(cls, filter_kwargs):
        return cls.objects.filter(**filter_kwargs)

    @classmethod
    def create_record(cls, kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def update_record(cls, filter_kwargs, update_kwargs):
        return cls.objects.filter(**filter_kwargs).update(**update_kwargs)
