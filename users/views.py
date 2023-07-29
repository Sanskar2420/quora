from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from users.services import RegisterUserService, LoginService, UpdateProfileService, FollowersService, \
    ListOfUsersService, FollowingService, DisplayAnotherUserProfileService, HomeViewService


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HomeViewService(request=request).get_view()


class RegisterUser(View):
    def get(self, request, *args, **kwargs):
        return RegisterUserService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return RegisterUserService(request=request).post_view()


class Login(View):
    def get(self, request, *args, **kwargs):
        return LoginService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return LoginService(request=request).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfile(View):
    def get(self, request, *args, **kwargs):
        return UpdateProfileService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return UpdateProfileService(request=request).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class Followers(View):
    def get(self, request, *args, **kwargs):
        return FollowersService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return FollowersService(request=request).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class ListOfUsers(View):
    def get(self, request, *args, **kwargs):
        return ListOfUsersService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return ListOfUsersService(request=request).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class Following(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return FollowingService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return FollowingService(request=request).post_view()


class DisplayAnotherUserProfile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return DisplayAnotherUserProfileService(request=request, id=kwargs.get("id")).get_view()
