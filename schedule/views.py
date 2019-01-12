import datetime

from django.views.generic import ListView
from django.db.models import Avg, Sum

from .models import Statistic

# Create your views here.


class PlayerStatsListView(ListView):
    model = Statistic
    template_name = 'player_stats_list.html'

    def get_queryset(self):
        stats = Statistic.objects.filter(
            competition__schedule__date__date=datetime.date(2019, 3, 10)
        )
        stats = stats.values('player__user__first_name', 'player__user__last_name',
                             'player__department', 'player__id')
        stats = stats.annotate(
            Avg('FGA'), Avg('FGM'), Avg('three_PA'), Avg('three_PM'),
            Avg('FTA'), Avg('FTM'), Avg('OR'), Avg('DR'), Avg('BS'),
            Avg('AST'), Avg('BLK'), Avg('STL'), Avg('TO'), Sum('MIN'),
            Sum('PTS'), MPG=Avg('MIN'), PPG=Avg('PTS'),
        )

        return stats
