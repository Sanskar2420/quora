# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chats.models import Messages
from users.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def save_message(self, message_data):
        return Messages.create_message(kwargs=message_data)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        receiver = text_data_json["receiver"]
        sender_name = text_data_json["sender_name"]
        time_message = self.save_message(message_data={'sender': sender, 'receiver': receiver, 'message': message})
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, 'sender': sender, 'receiver': receiver,
                                   'receiver_name': time_message.receiver.username,
                                   'sender_name': sender_name, 'time': time_message.time.strftime("%m/%d/%Y, %H:%M:%S")}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        receiver = event["receiver"]
        sender_name = event["sender_name"]
        time = event['time']
        receiver_name = event['receiver_name']
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, 'sender': sender, 'receiver': receiver,
                                        'sender_name_final': sender_name, 'time_final': time,'receiver_name_final':receiver_name}))
