import datetime

from django.views.generic import ListView, DetailView
from django.db.models import Avg, Sum

from .models import Statistic, Schedule


class PlayerStatsListView(ListView):
    model = Statistic
    template_name = 'player_stats_list.html'

    def get_queryset(self):
        stats = Statistic.objects.values('player__user__first_name', 'player__user__last_name',
                                         'player__department', 'player__id')
        stats = stats.annotate(
            Avg('FGA'), Avg('FGM'), Avg('three_PA'), Avg('three_PM'),
            Avg('FTA'), Avg('FTM'), Avg('OR'), Avg('DR'), Avg('BS'),
            Avg('AST'), Avg('BLK'), Avg('STL'), Avg('TO'), Sum('MIN'),
            Sum('PTS'), MPG=Avg('MIN'), PPG=Avg('PTS'),
        )

        return stats


class ScheduleListView(ListView):
    model = Schedule
    template_name = 'schedule_list.html'
    paginate_by = 10
    queryset = Schedule.objects.all().order_by('teams__id').order_by('-date')


class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = 'schedule_detail.html'
    queryset = Schedule.objects.all().order_by('teams__id')

    def get_context_data(self, **kwargs):
        context = super(ScheduleDetailView, self).get_context_data(**kwargs)
        stats = Statistic.objects.filter(
            competition__schedule=self.object).select_related('player__user')
        context['t1_stat'] = stats.filter(
            competition__team=self.object.teams.all()[0])
        context['t2_stat'] = stats.filter(
            competition__team=self.object.teams.all()[1])
        return context
