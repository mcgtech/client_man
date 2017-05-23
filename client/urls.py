from django.conf.urls import url
from . import views

urlpatterns = [
    # client crud
    url(r'^client/new/$', views.client_new, name='client_new'),
    url(r'^client/(?P<pk>\d+)/edit/$', views.client_edit, name='client_edit'),
    url(r'^client/(?P<pk>\d+)/$', views.client_detail, name='client_detail'),
    url(r'^client_search/$', views.client_search, name='client_search'),
    # contract crud
    # url(r'^contract/new/$', views.client_new, name='contract_new'),
    # searching
    url(r'^auto/quick_client_search/$', views.quick_client_search, name='quick_client_search'),
    # migration
    url(r'^load_clients/$', views.load_clients, name='load_clients'),
]