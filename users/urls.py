from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from users.views import RegisterUser, Login, UpdateProfile, Followers, ListOfUsers, Following, \
    DisplayAnotherUserProfile, HomeView, CreateChatRoom
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('profile/', UpdateProfile.as_view(), name='profile'),
    path('logout/', auth_view.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('followers/', Followers.as_view(), name='followers'),
    path('users/', ListOfUsers.as_view(), name='list-users'),
    path('following/', Following.as_view(), name='following'),
    path('displayProfile/<int:id>', DisplayAnotherUserProfile.as_view(), name='display-profile'),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name='password_reset.html',
             html_email_template_name='password_reset_email.html'
         ),
         name='password-reset'
         ),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    path('chatCreation/', CreateChatRoom.as_view(), name='chat-creation')
]
