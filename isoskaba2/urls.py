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
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', skabaviews.login_user, name='index'),
    url(r'^login', skabaviews.login_user, name='login'),
    url(r'^siteadmin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/$', skabaviews.admin_index, name='admin_index'),
    url(r'^admin/users/$', skabaviews.list_users, name='userlist'),
    url(r'^admin/events/$', skabaviews.list_events, name='eventlist'),
    url(r'^admin/events/add/$', skabaviews.event_add, name='event_add'),
    url(r'^admin/events/edit/(?P<event_slug>([a-z0-9-]+))/$', skabaviews.event_edit, name='event_edit'),
    url(r'^admin/attendances/$', skabaviews.verify_attendances, name='verify_attendances'),
    url(r'^admin/users/add', skabaviews.user_add, name='user_add'),
    url(r'^admin/users/import', skabaviews.user_import, name='user_import'),
    url(r'^admin/events/import', skabaviews.event_import, name='event_import'),
    url(r'^admin/users/edit/(?P<user_id>([0-9]+))/$', skabaviews.admin_edit, name='admin_edit'),
    url(r'^admin/guilds/populate', skabaviews.guilds_populate, name='guilds_populate'),
    url(r'^admin/guildpoints/populate', skabaviews.guild_points_populate, name='guild_points_populate'),
    url(r'^admin/guildpoints/update', skabaviews.guild_points_update, name='guild_points_update'),
    url(r'^logout/$', skabaviews.logout_user, name='logout'),
    url(r'^user/$', skabaviews.user_info, name='userinfo'),
    url(r'^user/edit/$', skabaviews.user_edit, name='user_edit'),
    url(r'^events/$', skabaviews.list_user_events, name='usereventlist'),
    url(r'^attend', skabaviews.attend_event, name='attend'),
    url(r'^deleteuser', skabaviews.delete_user, name='delete_user'),
    url(r'^deleteevent', skabaviews.delete_event, name='delete_event'),
    url(r'^guildranking/', skabaviews.guild_ranking, name='guild_ranking'),
    url(r'^userranking/', skabaviews.user_ranking, name='user_ranking'),
    url(r'^fixevents/', skabaviews.fix_events, name='fix_events'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
#    url(r'^scoreboard', skabaviews.scoreboard, name='scoreboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
