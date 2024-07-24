from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from main.forms import StyleFormMixin
from user.models import User
from django.contrib.auth.forms import PasswordResetForm


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        token = get_random_string(length=32)
        user.verification_token = token
        user.save()

        subject = 'Подтверждение почты'
        message = (f"Для подтверждения вашей учетной записи перейдите по ссылке: "
                   f"'http://127.0.0.1:8000/users/email/verification/{user.verification_token}/'")
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return user


class UserForm(StyleFormMixin, UserChangeForm):
    """Форма изменения пользователя"""

    class Meta:
        model = User
        fields = ('email', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class PermUserForm(StyleFormMixin, UserChangeForm):
    """Форма изменения пользователя если есть кастомные пермишены"""

    class Meta:
        model = User
        fields = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserPasswordResetForm(StyleFormMixin, PasswordResetForm):
    """Форма на сброс пароля"""

    class Meta:
        model = User
        fields = ('email',)