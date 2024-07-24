from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from main.models import NULLABLE


class User(AbstractUser):
    """Модель пользователя"""
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(verbose_name='Телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    verification_token = models.CharField(max_length=100, verbose_name='Токен верификации', **NULLABLE )
    is_verificated = models.BooleanField(default=False, verbose_name='Верификация')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            (
                'set_active',
                'Activate/deactivate user'
            )
        ]