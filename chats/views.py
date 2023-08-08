from django.contrib.auth.mixins import LoginRequiredMixin

# chat/views.py
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from chats.services import ChatRoomService


@method_decorator(csrf_exempt, name='dispatch')
class ChatRoom(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return ChatRoomService(request=request, kwargs=kwargs).get_view()
