import json
import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from questions.models import Questions, Answers
from users.models import User, FollowTable
from django.contrib import messages
from django.shortcuts import render, redirect

from users.constants import LOGIN_TEMPLATE, REGISTER_TEMPLATE, PROFILE_TEMPLATE, USER_EXISTS, USER_CREATED, \
    USERNAME_PATTERN, PASSWORD_PATTERN, EMAIL_PATTERN, INVALID_EMAIL_FORMAT, INVALID_PASSWORD_FORMAT, \
    INVALID_USERNAME_FORMAT, FIELDS_MISSING, SOMETHING_WENT_WRONG, ACCOUNT_DISABLED, INVALID_CREDENTIALS, \
    FOLLOWERS_TEMPLATE, LIST_OF_USER_TEMPLATE, FOLLOWING_TEMPLATE, DISPLAY_PROFILE_ONLY_TEMPLATE


class HomeViewService:
    def __init__(self, request):
        self.request = request

    def get_view(self):
        return redirect('login')


class RegisterUserService:
    def __init__(self, request):
        self.request = request
        self.template = REGISTER_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            return render(self.request, template_name=self.template, context=self.context)
        except Exception as err:
            print(f"Error : {err}")
            return redirect('login')

    def post_view(self):
        """
        Register a user by providing First Name, Last Name, Email, Username, Password, Superuser checkbox
        """
        try:
            self.context = {
                'user': User.get_user(filter_kwargs={"username": self.request.user.username})
            }

            firstname = self.request.POST.get('first').strip()
            lastname = self.request.POST.get('last').strip()
            email = self.request.POST.get('email').replace(" ", "")
            username = self.request.POST.get('username').replace(" ", "")
            password = self.request.POST.get('password').replace(" ", "")

            # check if username matches validation
            username_pattern = USERNAME_PATTERN
            if not re.match(username_pattern, username):
                self.context['error'] = INVALID_USERNAME_FORMAT
                return render(self.request, template_name=self.template, context=self.context)
            # check if password matches validation
            password_pattern = PASSWORD_PATTERN
            if not re.match(password_pattern, password):
                self.context['error'] = INVALID_PASSWORD_FORMAT
                return render(self.request, template_name=self.template, context=self.context)
            # check if email matches validation
            email_pattern = EMAIL_PATTERN
            if not re.match(email_pattern, email):
                self.context['error'] = INVALID_EMAIL_FORMAT
                return render(self.request, template_name=self.template, context=self.context)

            # Check if all the required data is available or not
            if firstname and lastname and email and username and password:
                user_email = User.get_user(filter_kwargs={"email": email})
                # If user with given email id not exist
                if not user_email:
                    user_name = User.get_user(filter_kwargs={"username": username})
                    # If user with given username not exist
                    if not user_name:
                        # Prepare data to create new user
                        user_data = {'first_name': firstname, 'last_name': lastname, 'username': username,
                                     'email': email, 'password': password}
                        # Create new user
                        msg = self.__save_new_user(user_details=user_data)
                        messages.success(self.request, msg)

                        # redirect user on Register new user page.
                        return redirect('login')
                    else:
                        # If user with given username exist show the error using messages
                        msg = USER_EXISTS.format(user_name.username)
                        messages.warning(self.request, msg)
                        return redirect('login')
                else:
                    # If user with given user email exist show the error using messages
                    msg = USER_EXISTS.format(user_email.email)
                    messages.warning(self.request, msg)
                    return redirect('login')
            else:
                msg = FIELDS_MISSING
                self.context['error'] = msg
                return render(self.request, template_name=self.template, context=self.context)
        except Exception as error:
            self.context['error'] = SOMETHING_WENT_WRONG
            return render(self.request, template_name=self.template, context=self.context)

    def __save_new_user(self, user_details):
        """
        Get the raw password and save it as new password.
        If details are valid and user gets created with user details, an email will be sent to the registered email address with
            username, raw password and link to change password
        @param user_details: User details like username, password, etc.
        """
        # Create copy of plain temporary password to send in email.
        plain_password = user_details.get('password')
        # Encrypts plain password/Creates a hash of password for security purpose.
        user_details['password'] = make_password(password=plain_password)
        obj = User.create_user(kwargs=user_details)
        return USER_CREATED.format(obj.username)


class LoginService:
    def __init__(self, request):
        self.request = request
        self.template = LOGIN_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            return render(self.request, template_name=self.template, context=self.context)
        except Exception as err:
            print(f"Error : {err}")
            return redirect('login')

    def post_view(self):
        """
        Take username and password from user.
        @return: redirect home if user is authenticated, 2fa if its enabled, error if no user found.
        """
        try:
            username = self.request.POST.get("username").replace(" ", "")
            password = self.request.POST.get("password").replace(" ", "")
            if self.request.user.is_authenticated:
                return redirect('show-question')
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                if not user.is_active:
                    self.context['error'] = ACCOUNT_DISABLED
                    return render(self.request, template_name=self.template, context=self.context)
                login(self.request, user)
                next_page = self.request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('show-question')
            else:
                self.context['error'] = INVALID_CREDENTIALS
                return render(self.request, template_name=self.template, context=self.context)
        except Exception as err:
            self.context['error'] = SOMETHING_WENT_WRONG
            return render(self.request, template_name=self.template, context=self.context)


class UpdateProfileService:
    def __init__(self, request):
        self.request = request
        self.template_name = PROFILE_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            self.context['user'] = User.get_user(filter_kwargs={"id": self.request.user.id})
            return render(self.request, template_name=self.template_name, context=self.context)
        except Exception as err:
            print(f"Error : {err}")
            return redirect('show-question')

    def post_view(self):
        try:
            data = json.loads(json.dumps(self.request.POST))
            user = User.get_user(filter_kwargs={"id": self.request.user.id})
            if data.get('password') and data.get('password') == data.get('re_type_password'):
                User.set_new_password(user=user, password=data.get('password'))
            User.update_user(filter_kwargs={"id": self.request.user.id},
                             update_kwargs={"first_name": data.get("firstname"), "last_name": data.get("lastname")})
            return redirect('profile')
        except Exception as err:
            self.context['user'] = User.get_user(filter_kwargs={"id": self.request.user.id})
            return render(self.request, template_name=self.template_name, context=self.context)


class FollowersService:

    def __init__(self, request):
        self.request = request
        self.template_name = FOLLOWERS_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            self.context['pending_users'] = FollowTable.get_users(
                filter_kwargs={"request_to": self.request.user.id, "status": "PENDING"})
            self.context['accepted_users'] = FollowTable.get_users(
                filter_kwargs={"request_to": self.request.user.id, "status": "ACCEPTED"})
            return render(self.request, template_name=self.template_name, context=self.context)
        except Exception as err:
            return redirect('show-question')

    def post_view(self):
        try:
            data = json.loads(self.request.body)
            FollowTable.update_record(
                filter_kwargs={"request_to": data.get("request_user"), "request_by": data.get("user_id")},
                update_kwargs={"status": "ACCEPTED" if bool(data.get("value")) else "REJECTED"})
            return JsonResponse({"msg": "Success"})
        except Exception as err:
            return JsonResponse({"msg": SOMETHING_WENT_WRONG})


class FollowingService:
    def __init__(self, request):
        self.request = request
        self.template_name = FOLLOWING_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            self.context['accepted_users'] = FollowTable.get_users(
                filter_kwargs={"request_by": self.request.user.id, "status": "ACCEPTED"})
            return render(self.request, template_name=self.template_name, context=self.context)
        except Exception as err:
            return redirect('show-question')

    def post_view(self):
        try:
            data = self.request.POST
            FollowTable.update_record(
                filter_kwargs={"request_to": data.get("user_id"), "request_by": self.request.user},
                update_kwargs={"status": "REJECTED"})
            return JsonResponse({"msg": "Success"})
        except Exception as err:
            return JsonResponse({"msg": SOMETHING_WENT_WRONG})


class ListOfUsersService:
    def __init__(self, request):
        self.request = request
        self.template_name = LIST_OF_USER_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            self.context['users'] = User.get_user_exclude(exclude_filter={"id__exact": self.request.user.id})
            return render(self.request, template_name=self.template_name, context=self.context)
        except Exception as err:
            return redirect('show-question')

    def post_view(self):
        try:
            data = json.loads(self.request.body)
            filter_kwargs = {"request_to": User.get_user(filter_kwargs={"id": data.get("user_id")}),
                             "request_by": self.request.user}
            if FollowTable.get_users(filter_kwargs=filter_kwargs):
                FollowTable.update_record(filter_kwargs=filter_kwargs, update_kwargs={"status": "PENDING"})
            else:
                record = FollowTable.create_record(
                    kwargs={"request_to": User.get_user(filter_kwargs={"id": data.get("user_id")}),
                            "request_by": self.request.user, "status": "PENDING"})
            return JsonResponse({"msg": "Success"})
        except Exception as err:
            return JsonResponse({"msg": SOMETHING_WENT_WRONG})


class DisplayAnotherUserProfileService:
    def __init__(self, request, id):
        self.request = request
        self.template_name = DISPLAY_PROFILE_ONLY_TEMPLATE
        self.context = {}
        self.id = id

    def get_view(self):
        self.context['user'] = User.get_user(filter_kwargs={"id": self.id})
        self.context['followers'] = FollowTable.get_users(
            filter_kwargs={"request_to": self.request.user, "status": "ACCEPTED"})
        self.context['following'] = FollowTable.get_users(
            filter_kwargs={"request_by": self.request.user, "status": "ACCEPTED"})
        self.context['questions'] = Questions.get_all_questions(kwargs={"user": self.request.user})
        self.context['answers'] = Answers.get_all_answers(kwargs={"user": self.request.user})
        return render(self.request, template_name=self.template_name, context=self.context)
