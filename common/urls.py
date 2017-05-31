from django.conf.urls import url
from . import views
# from common.views import *

urlpatterns = [
    # html template crud
    url(r'^html_temp/new/$', views.html_temp_new, name='html_temp_new'),
    url(r'^html_temp/(?P<pk>\d+)/edit/$', views.html_temp_edit, name='html_temp_edit'),
]