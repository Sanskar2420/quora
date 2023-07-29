from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from questions.services import AddQuestionService, ShowQuestionsService, QuestionLikeUnlikeService, \
    DetailQuestionService, AnswerLikeUnlikeService, CommentService, AnswerService, UserQuestionService


@method_decorator(csrf_exempt, name='dispatch')
class AddQuestion(View):
    def get(self, request, *args, **kwargs):
        return AddQuestionService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return AddQuestionService(request=request).post_view()


class ShowQuestions(View):
    def get(self, request, *args, **kwargs):
        return ShowQuestionsService(request=request).get_view()


@method_decorator(csrf_exempt, name='dispatch')
class DetailQuestion(View):
    def get(self, request, *args, **kwargs):
        return DetailQuestionService(request=request, question_id=kwargs.get("id")).get_view()

    def post(self, request, *args, **kwargs):
        return DetailQuestionService(request=request, question_id=kwargs.get("id")).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteQuestion(View):
    def post(self, request, *args, **kwargs):
        return DetailQuestionService(request=request, question_id=kwargs.get('id')).delete_view()


@method_decorator(csrf_exempt, name='dispatch')
class Comments(View):
    def get(self, request, *args, **kwargs):
        return CommentService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return CommentService(request=request).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class CommentDelete(View):
    def post(self, request, *args, **kwargs):
        return CommentService(request=request).delete_view()


@method_decorator(csrf_exempt, name='dispatch')
class Answers(View):
    def get(self, request, *args, **kwargs):
        return AnswerService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return AnswerService(request=request).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class AnswerDelete(View):
    def post(self, request, *args, **kwargs):
        return AnswerService(request=request).delete_view()


@method_decorator(csrf_exempt, name='dispatch')
class QuestionLikeUnlike(View):
    def post(self, request, *args, **kwargs):
        return QuestionLikeUnlikeService(request=request).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class AnswerLinkUnlike(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return AnswerLikeUnlikeService(request=request).post_view()


class UserQuestions(View):
    def get(self, request, *args, **kwargs):
        return UserQuestionService(request=request).get_view()
