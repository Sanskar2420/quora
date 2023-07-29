import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect

from questions.constants import ADD_QUESTION_TEMPLATE, SHOW_QUESTION_TEMPLATE, SHOW_DETAILED_QUESTION_TEMPLATE
from questions.models import Questions, Tags, QuestionTags, QuestionLike, AnswerLike, Comment as CommentModel, Answers, \
    Comment, AnswerDisLike, QuestionDisLike


class AddQuestionService:
    def __init__(self, request):
        self.request = request
        self.template_name = ADD_QUESTION_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            return render(self.request, template_name=self.template_name, context=self.context)
        except Exception as err:
            print(f"Error: {err}")
            return redirect('login')

    def post_view(self):
        try:
            data = self.request.POST
            question = self.__create_question(kwargs={'question': data.get('question', '')},
                                              tags=data.getlist('tags', []))
            return redirect('show-question')
        except Exception as err:
            print(f"Error: {err}")
            return render(self.request, template_name=self.template_name, context=self.context)

    def __create_question(self, kwargs, tags):
        kwargs.update({'user': self.request.user, "date_posted": datetime.now()})
        question = Questions.create_question(kwargs=kwargs)
        list_of_question_tags = [{"question": question, "tag": Tags.get_or_create_tags(kwargs={'name': tag.lower()})[0]}
                                 for tag in tags]
        QuestionTags.create_question_tag(kwargs=list_of_question_tags)
        return question


class ShowQuestionsService:
    def __init__(self, request):
        self.request = request
        self.template_name = SHOW_QUESTION_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            self.context['questions'] = Questions.get_all_questions()
            return render(self.request, template_name=self.template_name, context=self.context)
        except Exception as err:
            print(f"Error: {err}")
            return redirect('login')


class DetailQuestionService:
    def __init__(self, request, question_id):
        self.request = request
        self.template_name = SHOW_DETAILED_QUESTION_TEMPLATE
        self.context = {}
        self.question_id = question_id

    def get_view(self):
        try:
            question = Questions.get_all_questions(kwargs={"id": self.question_id})
            self.context['question'] = question.first() if question else {}
            self.context['answers'] = Answers.get_all_answers(
                kwargs={"question": question.first().id}) if question else []
            self.context['comments'] = Comment.get_all_comment(
                filter_kwargs={"question": question.first().id}) if question else []
            question_dict = {'question': question.first(),
                             'question_dislikes': QuestionDisLike.get_dislikes_for_question(
                                 kwargs={"question": question.first()}),
                             "question_likes": QuestionLike.get_likes_questions(kwargs={"question": question.first()}),
                             "tags": QuestionTags.get_all_tags(kwargs={"question": question.first()})}
            answer_list = []
            for answer in self.context.get('answers'):
                answer_dict = {"answer": answer,
                               "answer_dislike": AnswerDisLike.get_dislikes_for_answer(kwargs={"answer": answer}),
                               "answer_likes": AnswerLike.get_likes_for_answer(kwargs={"answer": answer})}
                answer_list.append(answer_dict)
            self.context['question_meta'] = question_dict
            self.context['answer_meta'] = answer_list
            return render(self.request, template_name=self.template_name, context=self.context)
        except Exception as err:
            print(f"Error: {err}")
            return redirect('login')

    def post_view(self):
        try:
            data = json.loads(json.dumps(self.request.POST))
            if len(Questions.get_all_questions(kwargs={"id": data.get("question_id"), "user": self.request.user})) >= 1:
                Questions.get_update_questions(filter_kwargs={"id": data.get("question_id")},
                                               update_kwargs={"question": data.get("description")})
                display = "Deleted Successfully."
            else:
                display = "You can't update this question."
            return JsonResponse({"msg": "Success", "display": display})
        except Exception as error:
            print(f"Error:{error}")
            return JsonResponse({"msg": "Error"})

    def delete_view(self):
        data = json.loads(self.request.body)
        question = Questions.get_all_questions(kwargs={'id': data.get('question_id')})
        if question and self.request.user.id == question.first().user.id:
            Questions.delete_question(filter_kwargs={"id": data.get('question_id')})
            return JsonResponse({'msg': 'Success'})
        return JsonResponse({'msg': "You can't delete"})


class QuestionLikeUnlikeService:
    def __init__(self, request):
        self.request = request

    def post_view(self):
        data = self.request.POST
        try:
            like_of_question, msg = self.__manage_likes(data=data)
            return JsonResponse({"msg": "Success", "total_number_likes": len(like_of_question), "display": msg})
        except Exception as err:
            question_id = data.get("id_of_question")
            if question_id:
                like_of_question = QuestionLike.get_likes_questions(kwargs={"question_id": question_id})
            else:
                like_of_question = []
            return JsonResponse({"msg": "Error", "total_number_likes": len(like_of_question)})

    def __manage_likes(self, data):
        question_id = data.get("id_of_question")
        if bool(int(data.get("like"))):
            questionlike, msg = QuestionLike.add_like(kwargs={'user': self.request.user, 'question_id': question_id})
        else:
            questiondislike, msg = QuestionDisLike.add_dislike(
                kwargs={'user': self.request.user, 'question_id': question_id})
        return QuestionLike.get_likes_questions(kwargs={"question": question_id}), msg


class AnswerLikeUnlikeService:
    def __init__(self, request):
        self.request = request

    def post_view(self):
        data = self.request.POST
        try:
            like_of_answer, msg = self.__manage_likes(data=data)
            return JsonResponse({"msg": "Success", "total_number_likes": len(like_of_answer), "display": msg})
        except Exception as err:
            answer_id = data.get("id_of_answer")
            if answer_id:
                like_of_answer = AnswerLike.get_likes_for_answer(kwargs={"answer": answer_id})
            else:
                like_of_answer = []
            return JsonResponse({"msg": "Error", "total_number_likes": len(like_of_answer)})

    def __manage_likes(self, data):
        answer_id = data.get("id_of_answer")
        if bool(int(data.get("like"))):
            answerlike, msg = AnswerLike.add_like(kwargs={'user': self.request.user, 'answer_id': answer_id})
        else:
            answerdislike, msg = AnswerDisLike.add_dislike(kwargs={'user': self.request.user, 'answer_id': answer_id})
        return AnswerLike.get_likes_for_answer(kwargs={"answer": answer_id}), msg


class CommentService:
    def __init__(self, request):
        self.request = request

    def get_view(self):
        return redirect('show-question')

    def post_view(self):
        try:
            data = json.loads(self.request.body)
            kwargs = {'question': Questions.get_all_questions(kwargs={'id': data.get("question_id")}).first(),
                      'description': data.get('description')}
            comment = self.__create_comment(kwargs=kwargs)
            return JsonResponse({"msg": "Success"})
        except Exception as err:
            print(f'Error : {err}')
            return JsonResponse({"msg": "Error"})

    def delete_view(self):
        data = json.loads(json.dumps(self.request.POST))
        comment = CommentModel.get_all_comment(filter_kwargs={'id': data.get('comment_id')})
        if comment and self.request.user.id in [
            comment.first().user.id,
            comment.first().question.user.id,
        ]:
            CommentModel.delete_comment(filter_kwargs={'id': data.get('comment_id')})
            return JsonResponse({'msg': 'Success'})
        return JsonResponse({'msg': "You can't delete"})

    def __create_comment(self, kwargs):
        kwargs.update({"user": self.request.user, "comment_date": datetime.now()})
        return CommentModel.create_comment(kwargs=kwargs)


class AnswerService:
    def __init__(self, request):
        self.request = request

    def get_view(self):
        return redirect('show-question')

    def post_view(self):
        try:
            data = json.loads(self.request.body)
            kwargs = {'question': Questions.get_all_questions(kwargs={'id': data.get("question_id")}).first(),
                      'answer': data.get('description')}
            answer = self.__create_answer(kwargs=kwargs)
            return JsonResponse({"msg": "Success"})
        except Exception as err:
            print(f'Error : {err}')
            return JsonResponse({"msg": "Error"})

    def delete_view(self):
        data = json.loads(json.dumps(self.request.POST))
        answer = Answers.get_all_answers(kwargs={'id': data.get('answer_id')})
        if answer and self.request.user.id in [
            answer.first().user.id,
            answer.first().question.user.id,
        ]:
            Answers.delete_answer(filter_kwargs={"id": data.get('answer_id')})
            return JsonResponse({'msg': 'Success'})
        return JsonResponse({'msg': "You can't delete"})

    def __create_answer(self, kwargs):
        kwargs.update({"user": self.request.user, "answer_date": datetime.now()})
        return Answers.create_answer(kwargs=kwargs)


class UserQuestionService:
    def __init__(self, request):
        self.request = request
        self.template_name = SHOW_QUESTION_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            user = self.request.user
            self.context['questions'] = Questions.get_all_questions(kwargs={'user': user.id})
            return render(self.request, template_name=self.template_name, context=self.context)
        except Exception as err:
            print(f"Error: {err}")
            return redirect('login')
