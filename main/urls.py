from django.urls import path

from main.views import DistributionTryListView, CustomerUpdateView, CustomerCreateView, CustomerListView, \
    DistributionDetailView, DistributionDeleteView, DistributionListView, DistributionCreateView, \
    DistributionUpdateView, CustomerDetailView, CustomerDeleteView

urlpatterns = [
    path('log/', DistributionTryListView.as_view(), name='log_list'),
    path('customer/edit/<int:pk>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/', CustomerListView.as_view(), name='customers_list'),
    path('distribution/<int:pk>/', DistributionDetailView.as_view(), name='distribution_detail'),
    path('delete/<int:pk>/', DistributionDeleteView.as_view(), name='distribution_delete'),
    path('', DistributionListView.as_view(), name='distribution_list'),
    path('create/', DistributionCreateView.as_view(), name='distribution_create'),
    path('edit/<int:pk>/', DistributionUpdateView.as_view(), name='distribution_edit'),
    path('customers/<int:pk>', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/delete/<int:pk>', CustomerDeleteView.as_view(), name='customer_delete'),
]