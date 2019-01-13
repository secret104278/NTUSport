"""NTUSport URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from schedule.views import PlayerStatsListView, ScheduleListView, ScheduleDetailView
from player.views import PlayerDetailView
from team.views import TeamListView, TeamDetailView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^scheduleList', ScheduleListView.as_view(), name='schedule'),
    url(r'^ScheduleDetail/(?P<pk>[0-9]+)',
        ScheduleDetailView.as_view(), name='schedule'),
    url(r'^playerDetail/(?P<pk>[0-9]+)',
        PlayerDetailView.as_view(), name='playerStats'),
    url(r'^playerStatsList', PlayerStatsListView.as_view(), name='playerStats'),
    url(r'^teamList', TeamListView.as_view(), name='teamStats'),
    url(r'^teamDetail/(?P<pk>[0-9]+)',
        TeamDetailView.as_view(), name='teamStats'),
    url(r'^', PlayerStatsListView.as_view(), name='playerStats'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
