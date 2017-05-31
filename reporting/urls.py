from django.conf.urls import url
from . import views

urlpatterns = [
    # reporting
    url(r'^show_report/(?P<entity_id>\d+)/(?P<report_id>\d+)/$', views.show_report, name='show_report'),
]