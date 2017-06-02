"""client_man URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse_lazy
from common import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', login, {'template_name': 'login.html'}, name='client_man_login'),
    url(r'^accounts/logout/$', logout, {'next_page': reverse_lazy('client_search')}, name='client_man_logout'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'', include('client.urls')),
    url(r'', include('common.urls')),
    url(r'', include('reporting.urls')),
    url(r'', include('email_template.urls')),
    url(r'^$', views.home_page, name='home_page'),
]
