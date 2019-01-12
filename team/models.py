from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from player.models import Student


class Team(models.Model):
    caption = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        related_name="lead_team",
        related_query_name="lead_team"
    )
    vice_caption = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        related_name="vice_lead_team",
        related_query_name="vice_lead_team"
    )
    managers = models.ManyToManyField(
        Student,
        related_name="manage_team",
        related_query_name="vice_leading_team"
    )
    players = models.ManyToManyField(Student)
    department = models.CharField(max_length=4)

    @property
    def comp_stat(self):
        win_num = 0
        loss_num = 0
        for comp in self.competition_set.all():
            if comp.schedule.win == self:
                win_num += 1
            else:
                loss_num += 1
        return win_num, loss_num

    def __str__(self):
        return '%s, Number of players: %i' % (self.department, self.players.count())

    def clean(self):
        if (self.caption and
                not self.caption.team_set.filter(id=self.id).exists()):
            raise ValidationError(
                _({'caption': 'The caption of a team should exist in team players.'})
            )
        if (self.vice_caption and
                not self.vice_caption.team_set.filter(id=self.id).exists()):
            raise ValidationError(
                _({'vice_caption': 'The vice caption of a team should ' +
                   'exist in team players.'})
            )
