from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^client/new/$', views.client_new, name='client_new'),
    url(r'^client/(?P<pk>\d+)/edit/$', views.client_edit, name='client_edit'),
    url(r'^client/(?P<pk>\d+)/$', views.client_detail, name='client_detail'),
    url(r'^client_search/$', views.client_search, name='client_search'),
    url(r'^auto/quick_client_search/$', views.quick_client_search, name='quick_client_search'),
    url(r'^load_clients/$', views.load_clients, name='load_clients'),
]