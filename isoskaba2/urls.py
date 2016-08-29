"""isoskaba2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from skaba import views as skabaviews
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    url(r'^$', skabaviews.index, name='index'),
    url(r'^siteadmin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/$', skabaviews.admin_index, name='admin_index'),
    url(r'^admin/users/$', skabaviews.list_users, name='userlist'),
    url(r'^admin/events/$', skabaviews.list_events, name='eventlist'),
    url(r'^admin/events/add/$', skabaviews.event_add, name='event_add'),
    url(r'^admin/events/edit/(?P<event_slug>([a-z0-9-]+))/$', skabaviews.event_edit, name='event_edit'),
    url(r'^admin/users/add', skabaviews.user_add, name='user_add'),
    url(r'^admin/guilds/populate', skabaviews.guilds_populate, name='guilds_populate'),
    url(r'^logout/$', skabaviews.logout_user, name='logout'),
    url(r'^login', skabaviews.login_user, name='login'),
    url(r'^events/$', skabaviews.list_user_events, name='usereventlist')
]
urlpatterns += i18n_patterns('',

)
