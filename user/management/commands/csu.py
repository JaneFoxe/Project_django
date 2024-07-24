from django.core.management import BaseCommand

from user.models import User


class Command(BaseCommand):
    """Создаем суперюзера для админки"""
    def handle(self, username=None,  *args, **options):
        user = User.objects.create(
            email='admin@admin.ru',
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        user.set_password('12345')
        user.save()