from django.contrib import admin

from django.contrib import admin

from main.models import Customer, Distribution, Message, DistributionTry


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Админка клиента"""
    list_display = ('pk', 'email', 'name')
    list_filter = ('name',)
    search_fields = ('email', 'name', 'message',)


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    """Админка рассылки"""
    list_display = ('pk', 'start_time', 'end_time', 'periodicity', 'status',)
    list_filter = ('start_time', 'end_time', 'periodicity', 'status',)
    search_fields = ('start_time', 'end_time',)


@admin.register(Message)
class MessageListSettingsAdmin(admin.ModelAdmin):
    """Админка сообщения"""
    list_display = ('pk', 'subject', 'mailing_list',)
    list_filter = ['mailing_list', ]
    search_fields = ['subject', 'content', ]


@admin.register(DistributionTry)
class LogAdmin(admin.ModelAdmin):
    """Админка логов"""
    list_display = ['pk', 'mailing_list', 'time', 'status', 'server_response', ]
    list_filter = ['mailing_list', 'status', ]
    search_fields = ['mailing_list', 'time', 'status', ]
