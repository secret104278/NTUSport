import datetime

from django.views.generic import ListView, DetailView
from django.db.models import Avg, Sum

from .models import Team
from schedule.models import Competition, Statistic
from player.models import Student


class TeamListView(ListView):
    model = Team
    template_name = "team_list.html"

    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        return context


class TeamDetailView(DetailView):
    model = Team
    template_name = "team_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        comps = Competition.objects.filter(team=self.object).values(
            'team__id')
        context['summary'] = Statistic.objects.filter(competition__team__id__in=comps).values(
            'competition__team__id').annotate(
            Avg('FGA'), Avg('FGM'), Avg('three_PA'), Avg('three_PM'),
            Avg('FTA'), Avg('FTM'), Avg('OR'), Avg('DR'), Avg('BS'),
            Avg('AST'), Avg('BLK'), Avg('STL'), Avg('TO'), Sum('MIN'),
            Sum('PTS'), MPG=Avg('MIN'), PPG=Avg('PTS'),
        ).first()

        rank = Statistic.objects.filter(competition__team__id__in=comps).values(
            'player__id').annotate(PTS=Avg('PTS'), FTM=Avg('FTM'), AST=Avg('AST'))
        highest_PTS_id = rank.order_by('PTS').first()['player__id']
        highest_FTM_id = rank.order_by('FTM').first()['player__id']
        highest_AST_id = rank.order_by('AST').first()['player__id']
        context['PTS'] = rank.order_by('PTS').first()['PTS']
        context['FTM'] = rank.order_by('FTM').first()['FTM']
        context['AST'] = rank.order_by('AST').first()['AST']
        context['highest_PTS'] = Student.objects.get(id=highest_PTS_id)
        context['highest_FTM'] = Student.objects.get(id=highest_FTM_id)
        context['highest_AST'] = Student.objects.get(id=highest_AST_id)

        return context
