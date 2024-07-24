from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Customer(models.Model):
    email = models.EmailField(max_length=150, unique=True, verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    message = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='owner_customer',
                              verbose_name="владелец", **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('name',)


class Distribution(models.Model):
    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_CHOICES = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
    ]

    start_time = models.DateTimeField(verbose_name='Время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Время окончания рассылки')
    periodicity = models.CharField(max_length=50, verbose_name='Периодичность', choices=PERIODICITY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=CREATED, verbose_name='Статус рассылки')

    customer = models.ManyToManyField(Customer, verbose_name='Клиенты рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='owner',
                              verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return f'time: {self.start_time} - {self.end_time}, periodicity: {self.periodicity}, status: {self.status},' \
               f'owner: {self.owner}'

    class Meta:
        verbose_name = 'Настройки рассылки'
        verbose_name_plural = 'Настройки рассылки'
        permissions = [
            (
                'change_status',
                'Can change status'
            )
        ]


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Тело письма')
    mailing_list = models.ForeignKey(Distribution, on_delete=models.CASCADE, verbose_name='Рассылка',
                                     related_name='messages', **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class DistributionTry(models.Model):
    time = models.DateTimeField(verbose_name='Дата и время последней попытки', auto_now_add=True)
    status = models.BooleanField(verbose_name='Статус попытки')
    server_response = models.CharField(verbose_name='Ответ почтового сервера', **NULLABLE)

    mailing_list = models.ForeignKey(Distribution, on_delete=models.CASCADE, verbose_name='Рассылка')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент рассылки')

    def __str__(self):
        return f'{self.time} {self.status}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
