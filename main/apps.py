import time
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from django.apps import AppConfig


def sending_mail():
    """Вызов кастомной команды рассылки"""
    call_command('sending_mail')


def start_scheduler():
    """Старт рассылки с интервалом проверки"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(sending_mail, 'interval', minutes=0.1)
    scheduler.start()


class DistributionConfig(AppConfig):
    """Запуск рассылки при запуске сервера"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        time.sleep(2)
        start_scheduler()
