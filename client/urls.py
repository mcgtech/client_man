from django.conf.urls import url
from . import views
from django_filters.views import FilterView
from client.models import Client
from client.filters import ClientFilter
from client.views import ClientViewFilter

urlpatterns = [
    # client crud
    url(r'^client/new/$', views.client_new, name='client_new'),
    url(r'^client/(?P<pk>\d+)/edit/$', views.client_edit, name='client_edit'),
    url(r'^client/(?P<pk>\d+)/$', views.client_detail, name='client_detail'),
    # contract crud
    url(r'^contract/(?P<client_pk>\d+)/new/$', views.contract_new, name='contract_new'),
    url(r'^contract/(?P<client_pk>\d+)/(?P<contract_id>\d+)/edit/$', views.contract_edit, name='contract_edit'),
    # searching
    url(r'^client_search_old/$', views.client_search_old, name='client_search_old'),
    url(r'^client_search/$', ClientViewFilter.as_view(), name='client_search'),
    url(r'^auto/quick_client_search/$', views.quick_client_search, name='quick_client_search'),
    # migration
    url(r'^load_clients/$', views.load_clients, name='load_clients'),
]