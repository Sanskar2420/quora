from django.shortcuts import render

from chats.models import Room, Messages
from users.models import User


class ChatRoomService:
    def __init__(self, request, kwargs):
        self.request = request
        self.template_name = 'chats/room.html'
        self.context = {}
        self.kwargs = kwargs

    def get_view(self):
        room = Room.get_room(kwargs={'name': self.kwargs.get('room_name')})
        if room:
            room = room.first()
        sender = self.request.user.id
        sender_name = User.get_user(filter_kwargs={'id': sender}).username
        receiver = room.sender.id if room.receiver.id == sender else room.receiver.id
        messages = Messages.get_all_messages(kwargs={'sender': sender, 'receiver': receiver})
        self.context = {'room_name': self.kwargs.get('room_name'), 'sender_id': sender, 'receiver_id': receiver,
                        'messages': messages, 'sender_name': sender_name, 'chat_with': list({room.receiver.username, room.sender.username}-{self.request.user.username})[0]}
        return render(self.request, template_name=self.template_name, context=self.context)
