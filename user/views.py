import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail

from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, FormView, TemplateView, ListView, DetailView

from user.forms import UserRegisterForm, UserForm, UserPasswordResetForm, PermUserForm
from user.models import User
from django.urls import reverse_lazy


class LoginView(BaseLoginView):
    """Вход"""
    template_name = 'user/login.html'

    def form_valid(self, form):
        email = form.get_user()
        user = User.objects.get(email=email)
        if not user.is_verificated:
            messages.error(self.request, 'Ваш email не верифицирован. Верифицируйте его с помощью ссылки в письме.')
            return redirect('user:login')
        return super().form_valid(form)


class LogoutView(BaseLogoutView):
    """Выход"""
    pass


class RegisterView(CreateView):
    """Регистрация"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('user:login')

    template_name = 'user/register.html'


def email_verification(request, token):
    """Верификация мыла"""
    try:
        user = User.objects.get(verification_token=token)
        user.is_verificated = True
        user.save()
        return redirect('user:login')
    except User.DoesNotExist:
        raise Http404("User does not exist")


class UserUpdateView(UpdateView):
    """Обновление пользователя"""
    model = User
    success_url = reverse_lazy('user:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(FormView):
    """Сброс пароля"""
    template_name = 'user/user_password_reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('user:user_password_message')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()

        if user is not None:
            characters = string.ascii_letters + string.digits
            new_password = ''.join(random.choice(characters) for i in range(12))

            user.password = make_password(new_password)
            user.save()

            subject = 'Восстановление пароля'
            message = f'Ваш новый пароль: {new_password}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return super().form_valid(form)


class UserPasswordSentView(TemplateView):
    """Отправка пароля"""
    template_name = 'user/user_password_message.html'


class UserListView(PermissionRequiredMixin, ListView):
    """Просмотр пользователей"""
    model = User
    permission_required = 'user.view_user'


class UserDetailView(PermissionRequiredMixin, DetailView):
    """Детальный просмотр пользователя"""
    model = User
    permission_required = 'user.view_user'


class UserMngUpdateView(UpdateView):
    """Изменение активности пользователя при наличии пермишена"""
    model = User
    success_url = reverse_lazy('user:user')
    form_class = PermUserForm

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)
