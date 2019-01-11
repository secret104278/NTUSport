import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .departments import Department


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    student_id = models.CharField(max_length=10)
    department = models.CharField(
        max_length=4,
        choices=Department.DEPARTMENT_CHOICE
    )
    grade = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return '%s%s %s %s' % (
            self.user.last_name,
            self.user.first_name,
            self.department,
            self.student_id
        )

    def clean(self):
        self.student_id = self.student_id.lower()

        # Formate Detail:
        # http://www.aca.ntu.edu.tw/aca2012/reg/services/serno.htm
        pattern = re.compile(r"([brdetacsyzpjfqhkmn])\d{8}")
        if not pattern.match(self.student_id):
            raise ValidationError(
                {'student_id': _('Student ID should begin with one of ' +
                                 '[B R D E T A C S Y Z P J F Q H K M N] with 8 digits. ' +
                                 '(Inconsistent in upper and lower case)')}
            )

        if self.grade > 6 or self.grade == 0:
            raise ValidationError(
                {'grade': _('Grade cannot be greater than 6 or equal 0.')}
            )

        self.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    assert sender == User
    if instance.groups.filter(name='Student').exists():
        instance.student.save()
