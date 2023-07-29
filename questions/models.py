from users.models import User
from django.db import models


# Create your models here.
class Questions(models.Model):
    question = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, null=False, default=1, on_delete=models.CASCADE, related_name='user')
    date_posted = models.DateTimeField(null=False, blank=False)
    is_deleted = models.BooleanField(default=False)

    @classmethod
    def create_question(cls, kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def get_all_questions(cls, kwargs=None):
        if kwargs is None:
            kwargs = {}
        kwargs["is_deleted"] = False
        return cls.objects.filter(**kwargs)

    @classmethod
    def get_update_questions(cls, filter_kwargs, update_kwargs):
        return cls.objects.filter(**filter_kwargs).update(**update_kwargs)

    @classmethod
    def delete_question(cls, filter_kwargs):
        cls.objects.filter(**filter_kwargs).update(**{"is_deleted": True})
        QuestionLike.objects.filter(**{"question": filter_kwargs.get("id")}).delete()
        AnswerLike.objects.filter(**{"answer__question": filter_kwargs.get("id")}).delete()
        Comment.objects.filter(**{"question": filter_kwargs.get("id")}).delete()
        return Answers.objects.filter(**{"question": filter_kwargs.get("id")}).delete()


class Tags(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)

    @classmethod
    def create_tag(cls, kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def get_tag(cls, kwargs=None):
        if not kwargs:
            kwargs = {}
        return cls.objects.filter(**kwargs)

    @classmethod
    def get_or_create_tags(cls, kwargs):
        return cls.objects.get_or_create(**kwargs)


class QuestionTags(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='question_tags')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='tag_of_question')

    @classmethod
    def create_question_tag(cls, kwargs):
        list_question_tags = [QuestionTags(question=i.get('question'), tag=i.get('tag')) for i in kwargs]
        return cls.objects.bulk_create(list_question_tags)

    @classmethod
    def get_all_tags(cls, kwargs):
        return cls.objects.filter(**kwargs)


class QuestionLike(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=False, related_name='question_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_like_question')

    @classmethod
    def add_like(cls, kwargs):
        if len(cls.objects.filter(**kwargs)) < 1:
            cls.objects.create(**kwargs)
            return QuestionDisLike.objects.filter(**kwargs).delete(), "You successfully liked this post."
        else:
            return cls.remove_like(filter_kwargs=kwargs), "You have successfully removed your like."

    @classmethod
    def remove_like(cls, filter_kwargs):
        if len(cls.objects.filter(**filter_kwargs)) < 1:
            return cls.add_like(kwargs=filter_kwargs)
        return cls.objects.filter(**filter_kwargs).delete()

    @classmethod
    def get_likes_questions(cls, kwargs):
        return cls.objects.filter(**kwargs)


class Comment(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=False, related_name='question_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_comment')
    description = models.CharField(null=True, blank=True, max_length=100)
    comment_date = models.DateTimeField(null=False)

    @classmethod
    def create_comment(cls, kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def update_comment(cls, filter_kwargs, update_kwargs):
        return cls.objects.filter(**filter_kwargs).update(**update_kwargs)

    @classmethod
    def delete_comment(cls, filter_kwargs):
        return cls.objects.filter(**filter_kwargs).delete()

    @classmethod
    def get_all_comment(cls, filter_kwargs):
        if filter_kwargs is None:
            filter_kwargs = {}
        return cls.objects.filter(**filter_kwargs)


class Answers(models.Model):
    answer = models.TextField(max_length=1000, null=False, blank=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=False, related_name='question_answer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_answer')
    review = models.IntegerField(default=0)
    answer_date = models.DateTimeField(null=False)
    is_deleted = models.BooleanField(default=False)

    @classmethod
    def get_all_answers(cls, kwargs):
        if kwargs is None:
            kwargs = {}
        kwargs['is_deleted'] = False
        return cls.objects.filter(**kwargs)

    @classmethod
    def create_answer(cls, kwargs):
        return cls.objects.create(**kwargs)

    @classmethod
    def delete_answer(cls, filter_kwargs):
        return cls.objects.filter(**filter_kwargs).update(**{"is_deleted": True})

    @classmethod
    def update_answer(cls, filter_kwargs, update_kwargs):
        return cls.objects.filter(**filter_kwargs).update(**update_kwargs)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE, null=False, related_name='answer_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_like_answer')

    @classmethod
    def add_like(cls, kwargs):
        if len(cls.objects.filter(**kwargs)) < 1:
            cls.objects.create(**kwargs)
            return AnswerDisLike.objects.filter(**kwargs).delete(), "You successfully liked this post."
        else:
            return cls.remove_like(filter_kwargs=kwargs), "You have successfully removed your like."

    @classmethod
    def remove_like(cls, filter_kwargs):
        return cls.objects.filter(**filter_kwargs).delete()

    @classmethod
    def get_likes_for_answer(cls, kwargs):
        return cls.objects.filter(**kwargs)


class AnswerDisLike(models.Model):
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE, null=False, related_name='answer_dislike')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_dislike_answer')

    @classmethod
    def add_dislike(cls, kwargs):
        if len(cls.objects.filter(**kwargs)) < 1:
            cls.objects.create(**kwargs)
            return AnswerLike.objects.filter(**kwargs).delete(), "You have successfully disliked."
        else:
            return cls.remove_dislike(filter_kwargs=kwargs), "You have successfully removed your dislike"

    @classmethod
    def remove_dislike(cls, filter_kwargs):
        return cls.objects.filter(**filter_kwargs).delete()

    @classmethod
    def get_dislikes_for_answer(cls, kwargs):
        return cls.objects.filter(**kwargs)


class QuestionDisLike(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=False, related_name='question_dislike')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_dislike_question')

    @classmethod
    def add_dislike(cls, kwargs):
        if len(cls.objects.filter(**kwargs)) < 1:
            cls.objects.create(**kwargs)
            return QuestionLike.objects.filter(**kwargs).delete(), "You have successfully disliked."
        else:
            return cls.remove_dislike(filter_kwargs=kwargs), "You have successfully removed your dislike"

    @classmethod
    def remove_dislike(cls, filter_kwargs):
        return cls.objects.filter(**filter_kwargs).delete()

    @classmethod
    def get_dislikes_for_question(cls, kwargs):
        return cls.objects.filter(**kwargs)
