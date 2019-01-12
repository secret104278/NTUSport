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
        context['summary'] = Statistic.objects.filter(player=self.object).values('player__id').annotate(
            Avg('FGA'), Avg('FGM'), Avg('three_PA'), Avg('three_PM'),
            Avg('FTA'), Avg('FTM'), Avg('OR'), Avg('DR'), Avg('BS'),
            Avg('AST'), Avg('BLK'), Avg('STL'), Avg('TO'), Sum('MIN'),
            Sum('PTS'), MPG=Avg('MIN'), PPG=Avg('PTS'),
        ).first()

        return context
