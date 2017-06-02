from django.conf.urls import url
from reporting.views import *

urlpatterns = [
    # reporting
    url(r'^show_report/(?P<entity_ids>\d+(,\d+)*)/(?P<report_id>\d+)/$', show_report, name='show_report'),
    # html template crud
    url(r'^report_temp/new/$', report_temp_new, name='report_temp_new'),
    url(r'^report_temp/(?P<pk>\d+)/edit/$', report_temp_edit, name='report_temp_edit'),
    # searching
    url(r'^report_temp_search/$', ReportTempSearch.as_view(), name='report_temp_search'),
]