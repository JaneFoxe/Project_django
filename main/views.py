from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.models import Blog
from main.forms import CustomerForm, DistributionForm, MessageForm, PermDistributionForm
from main.models import Customer, Distribution, Message, DistributionTry


class CustomerListView(LoginRequiredMixin, ListView):
    """Список клиентов"""
    model = Customer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Customer.objects.all()
        else:
            return Customer.objects.filter(owner=self.request.user)


class CustomerCreateView(LoginRequiredMixin, CreateView):
    """Создание клиента"""
    model = Customer
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('main:customer_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Обновление клиента"""
    model = Customer
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('main:customers_list')

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or self.request.user == client.owner


class CustomerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Просмотр одного клиента"""
    model = Customer

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or self.request.user == client.owner


class CustomerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление клиента"""
    model = Customer
    success_url = reverse_lazy('main:customers_list')

    def test_func(self):
        client = self.get_object()
        return self.request.user.is_superuser or self.request.user == client.owner


class DistributionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Просмотр одной рассылки"""
    model = Distribution

    def test_func(self):
        mailing_settings = self.get_object()
        return (self.request.user.is_superuser or self.request.user == mailing_settings.owner or
                self.request.user.has_perm(
                    'main.view_mailingsettings'))


class DistributionListView(LoginRequiredMixin, ListView):
    """Просмотр списка рассылок"""
    model = Distribution

    def cache_example(self):
        if settings.CACHE_ENABLED:
            key = f'mailset_list'
            mailset_list = cache.get(key)
            print(mailset_list)
            if mailset_list is None:
                mailset_list = Distribution.objects.all()
                cache.set(key, mailset_list)
        else:
            mailset_list = Distribution.objects.all()
        return mailset_list

    def get_queryset(self):
        return self.cache_example()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        user = self.request.user
        if user.is_superuser:
            context_data['all'] = Distribution.objects.count()
            context_data['active'] = Distribution.objects.filter(status=Distribution.STARTED).count()
            mailing_list = context_data['object_list']
            clients = [[client.email for client in mailing.clients.all()] for mailing in mailing_list]
            context_data['clients_count'] = len(clients)
        else:
            mailing_list = Distribution.objects.filter(owner=user)
            clients = [[client.email for client in mailing.clients.all()] for mailing in mailing_list]
            context_data['all'] = mailing_list.count()
            context_data['active'] = mailing_list.filter(status=Distribution.STARTED).count()
            context_data['clients_count'] = len(clients)
        random_blogs = Blog.objects.order_by('?')[:3]
        article_titles = [blog.title for blog in random_blogs]
        article_pk = [blog.pk for blog in random_blogs]
        context_data['articles'] = dict(zip(article_titles, article_pk))
        return context_data


class DistributionCreateView(LoginRequiredMixin, CreateView):
    """Создание рассылки"""
    model = Distribution
    form_class = DistributionForm
    success_url = reverse_lazy('main:distribution_list')

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Distribution, Message, extra=1, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST)
        else:
            context_data['formset'] = MessageFormset()

        return context_data

    def get_success_url(self):
        return reverse('main:distribution_list')


class DistributionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление рассылки"""
    model = Distribution
    permission_required = 'main.delete_mailingsettings'

    def test_func(self):
        mailing_settings = self.get_object()
        return self.request.user.is_superuser or self.request.user == mailing_settings.owner

    def get_success_url(self):
        return reverse('distribution:distribution_list')


class DistributionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Обновление рассылки"""
    model = Distribution
    form_class = DistributionForm

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.has_perm('main.change_status')

    def get_form_class(self):
        if self.request.user.has_perm('main.change_status') and not self.request.user.is_superuser:
            return PermDistributionForm
        return DistributionForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(Distribution, Message, extra=1, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:distribution_detail', args=[self.object.pk])


class DistributionTryListView(LoginRequiredMixin, ListView):
    """Просмотр списка логов"""
    model = DistributionTry

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        mailing_list = Distribution.objects.filter(owner=user).first()
        if user.is_superuser:
            context_data['all'] = DistributionTry.objects.count()
            context_data['success'] = DistributionTry.objects.filter(
                status=True).count()
            context_data['error'] = DistributionTry.objects.filter(status=False).count()
        else:
            user_logs = DistributionTry.objects.filter(mailing_list=mailing_list)
            context_data['all'] = user_logs.count()
            context_data['success'] = user_logs.filter(
                status=True).count()
            context_data['error'] = user_logs.filter(status=False).count()
        return context_data