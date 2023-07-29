from django.urls import path

from questions.views import AddQuestion, ShowQuestions, DetailQuestion, Comments, Answers, CommentDelete, AnswerDelete, \
    DeleteQuestion, AnswerLinkUnlike, UserQuestions, QuestionLikeUnlike

urlpatterns = [
    path('addQuestion/', AddQuestion.as_view(), name='add-question'),
    path('showQuestions/', ShowQuestions.as_view(), name='show-question'),
    path('question/<int:id>/', DetailQuestion.as_view(), name='detail-question'),
    path('comment/', Comments.as_view(), name='comment'),
    path('answer/', Answers.as_view(), name='answer'),
    path('commentDelete/', CommentDelete.as_view(), name='comment-delete'),
    path('answerDelete/', AnswerDelete.as_view(), name='answer-delete'),
    path('questionDelete/<int:id>', DeleteQuestion.as_view(), name='question-delete'),
    path('answerLikeUnlike/', AnswerLinkUnlike.as_view(), name='answer-like-unlike'),
    path('questionLikeUnlike/', QuestionLikeUnlike.as_view(), name='question-like-unlike'),
    path('UserQuestions/', UserQuestions.as_view(), name='user-question')
]
