from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from team.models import Team
from player.models import Student


class Schedule(models.Model):
    teams = models.ManyToManyField(
        Team,
        through='Competition',
        through_fields=('schedule', 'team')
    )
    referees = models.ManyToManyField(Student)
    date = models.DateTimeField()

    def __str__(self):
        comps = Competition.objects.filter(schedule=self).order_by('team')
        assert comps.count() == 2
        return '%s %s v.s. %s' % (self.date, comps[0].team.department, comps[1].team.department)

    def clean(self):
        if not self.referees.all().values_list(
            "department"
        ).union(
                self.teams.all().values_list(
                    "department"
                )).empty():
            raise ValidationError(
                {'referees': _('Referees cannot be in same department ' +
                               'with the racing team.')}
            )

        if self.teams_set.count() != 2:
            raise ValidationError(
                _('One schedule should envlove only two teams.')
            )


class Competition(models.Model):
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )
    players = models.ManyToManyField(
        Student,
        through='Statistic',
        through_fields=('competition', 'player')
    )

    def __str__(self):
        return '[%s] %s Number of %i players join' % (
            self.schedule, self.team.department, self.players.count()
        )

    def clean(self):
        if not self.players.team_set.exclude(id=self.team).empty():
            raise ValidationError(
                _({'players': 'All player should be in the same team.'})
            )


class Statistic(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.SET_NULL,
        null=True
    )
    player = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    MIN = models.PositiveSmallIntegerField(
        verbose_name='minutes',
        default=0
    )
    PTS = models.PositiveSmallIntegerField(
        verbose_name='points',
        default=0
    )
    FGA = models.PositiveSmallIntegerField(
        verbose_name='field goal attempts',
        default=0
    )
    FGM = models.PositiveSmallIntegerField(
        verbose_name='field goal made',
        default=0
    )
    three_PA = models.PositiveSmallIntegerField(
        verbose_name='3-pointer attempts',
        default=0
    )
    three_PM = models.PositiveSmallIntegerField(
        verbose_name='3-pointer made',
        default=0
    )
    FTA = models.PositiveSmallIntegerField(
        verbose_name='free throw attempts',
        default=0
    )
    FTM = models.PositiveSmallIntegerField(
        verbose_name='free throw made',
        default=0
    )
    OR = models.PositiveSmallIntegerField(
        verbose_name='offensive rebounds',
        default=0
    )
    DR = models.PositiveSmallIntegerField(
        verbose_name='defensive rebounds',
        default=0
    )
    BS = models.PositiveSmallIntegerField(
        verbose_name='block shoots',
        default=0
    )
    AST = models.PositiveSmallIntegerField(
        verbose_name='assists',
        default=0
    )
    BLK = models.PositiveSmallIntegerField(
        verbose_name='blocks',
        default=0
    )
    STL = models.PositiveSmallIntegerField(
        verbose_name='steals',
        default=0
    )
    TO = models.PositiveSmallIntegerField(
        verbose_name='turnovers',
        default=0
    )

    def __str__(self):
        return '[%s] %s' % (self.competition.schedule, self.player)
