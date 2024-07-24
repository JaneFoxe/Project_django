from django.forms import ModelForm

from main.models import Customer, Message, Distribution


class StyleFormMixin:
    """Миксин"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DistributionForm(StyleFormMixin, ModelForm):
    """Форма настроек рассылки"""
    class Meta:
        model = Distribution
        fields = ('start_time', 'end_time', 'periodicity', 'status', 'customer',)


class PermDistributionForm(StyleFormMixin, ModelForm):
    """Форма настроек рассылки для тех у кого частичные разрешения"""
    class Meta:
        model = Distribution
        fields = ('status', )


class MessageForm(StyleFormMixin, ModelForm):
    """Форма сообщений"""
    class Meta:
        model = Message
        fields = ('subject', 'content',)


class CustomerForm(StyleFormMixin, ModelForm):
    """Форма клиента"""
    class Meta:
        model = Customer
        fields = ('name', 'email', 'message',)