from django.urls import path

from chats import views

urlpatterns = [
    path("<str:room_name>/", views.ChatRoom.as_view(), name="room"),
]
