from django.conf.urls import url
from . import views
from .views import EmailTempSearch

urlpatterns = [
    # html template crud
    url(r'^email_temp/new/$', views.email_temp_new, name='email_temp_new'),
    url(r'^email_temp/(?P<pk>\d+)/edit/$', views.email_temp_edit, name='email_temp_edit'),
    # searching
    url(r'^email_temp_search/$', EmailTempSearch.as_view(), name='email_temp_search'),
    # testing
    url(r'^email_temp_test/(?P<temp_id>\d+)/(?P<client_id>\d+)/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.email_temp_test, name='email_temp_test'),
]