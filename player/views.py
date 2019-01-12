import math

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Sum

from .models import Student
from schedule.models import Statistic


class PlayerDetailView(DetailView):
    model = Student
    template_name = 'player_stats_detail.html'

    def get_object(self, queryset=None):
        student = Student.objects.select_related(
            'user')
        student = get_object_or_404(student, pk=self.kwargs['pk'])
        return student

    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        stats = Statistic.objects.filter(
            player=self.object)
        context['summary'] = stats.values('player__id').annotate(
            Avg('FGA'), Avg('FGM'), Avg('three_PA'), Avg('three_PM'),
            Avg('FTA'), Avg('FTM'), Avg('OR'), Avg('DR'), Avg('BS'),
            Avg('AST'), Avg('BLK'), Avg('STL'), Avg('TO'), Sum('MIN'),
            Sum('PTS'), MPG=Avg('MIN'), PPG=Avg('PTS'),
        ).first()
        PTS = [stat.PTS for stat in stats][:10]
        context['PTS'] = PTS
        context['PTS_high'] = max(PTS)+5
        context['PTS_delta'] = abs(sum(PTS) / (len(PTS))-PTS[-1])
        context['PTS_increase'] = sum(PTS) / len(PTS) < PTS[-1]

        REB = [(stat.OR + stat.DR) for stat in stats][:10]
        context['REB'] = REB
        context['REB_high'] = max(REB)+5
        context['REB_delta'] = abs(sum(REB) / (len(REB))-REB[-1])
        context['REB_increase'] = sum(REB) / len(REB) < REB[-1]

        return context
